# ---------- APPENDED INTEGRATION BLOCK START ----------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys, cv2, os, time, random, pickle, traceback
from typing import Any, Dict, List, Tuple, Optional
import pygame
from pygame.examples.music_drop_fade import play_file
import os, sys, pygame, time, math, random
from pathlib import Path


# ====================================================
# 🎬 RENK UYUMLU ANİMASYONLU VERİ KAYDETME PANELİ + MÜZİK
# ====================================================
def start_permission_panel_animated():
    SAVE_FOLDER_NAME = "AtagulDonerData"

    pygame.init()
    pygame.mixer.init()

    # 🎵 Müzik yükleme (assets klasöründen)
    music_loaded = False
    for file_name in ["izin.mp3", "izin.ogg", "izin.wav"]:
        path = os.path.join("assets", file_name)
        if os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play(-1)  # döngüde çal
                print(f"[BİLGİ] '{path}' başarıyla yüklendi ve çalıyor.")
                music_loaded = True
                break
            except Exception as e:
                print(f"[UYARI] {file_name} yüklenemedi: {e}")
    if not music_loaded:
        print("[UYARI] assets klasöründe izin.mp3 / .ogg / .wav bulunamadı veya çalınamadı.")

    # Ekran boyutu
    try:
        info = pygame.display.Info()
        W, H = info.current_w, info.current_h
    except:
        W, H = 1280, 720

    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Atagul Doner - Veri Kaydetme İzni (Animasyonlu)")
    clock = pygame.time.Clock()

    # Yazı tipleri
    title_font = pygame.font.SysFont("Segoe UI", max(36, W//40), bold=True)
    body_font  = pygame.font.SysFont("Segoe UI", max(20, W//85))
    btn_font   = pygame.font.SysFont("Segoe UI", max(22, W//70), bold=True)

    # Butonlar
    btn_w, btn_h = max(180, W//10), max(56, H//18)
    yes_rect = pygame.Rect(W//2 - btn_w - 30, H//2 + 100, btn_w, btn_h)
    no_rect  = pygame.Rect(W//2 + 30, H//2 + 100, btn_w, btn_h)

    # Parçacıklar
    particles = []
    for _ in range(45):
        particles.append([
            random.uniform(0, W),
            random.uniform(0, H),
            random.uniform(-0.2, 0.2),
            random.uniform(-0.05, 0.05),
            random.uniform(2, 8),
            random.uniform(0, math.pi * 2)
        ])

    start_t = time.time()
    accepted = None

    # Arka plan gradient
    def draw_gradient(t):
        for y in range(0, H, 3):
            r = max(0, min(255, int(30 + 20 * math.sin(t * 0.3 + y * 0.005))))
            g = max(0, min(255, int(80 + 100 * math.sin(t * 0.4 + y * 0.006))))
            b = max(0, min(255, int(100 + 80 * math.cos(t * 0.3 + y * 0.007))))
            pygame.draw.rect(screen, (r, g, b), (0, y, W, 3))

    # Cam efekti kart
    def glass_card():
        cw = min(960, W - 160)
        ch = min(460, H - 220)
        cx, cy = (W - cw) // 2, (H - ch) // 2
        card = pygame.Surface((cw, ch), pygame.SRCALPHA)
        for i in range(10):
            alpha = int(18 - i * 1.5)
            pygame.draw.rect(card, (255, 255, 255, alpha),
                             (i, i, cw - 2 * i, ch - 2 * i),
                             border_radius=18)
        card.fill((255, 255, 255, 35), special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(card, (cx, cy))
        return pygame.Rect(cx, cy, cw, ch)

    # Döngü
    while accepted is None:
        t = time.time() - start_t
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                accepted = False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_y:
                    accepted = True
                if ev.key in (pygame.K_n, pygame.K_ESCAPE):
                    accepted = False
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                if yes_rect.collidepoint((mx, my)):
                    accepted = True
                if no_rect.collidepoint((mx, my)):
                    accepted = False

        # Arka plan ve partiküller
        draw_gradient(t)
        for p in particles:
            p[0] += p[2]
            p[1] += p[3]
            p[5] += 0.02
            if p[0] < 0: p[0] = W
            if p[0] > W: p[0] = 0
            if p[1] < 0: p[1] = H
            if p[1] > H: p[1] = 0
            alpha = 150 + int(60 * math.sin(p[5]))
            pygame.draw.circle(screen, (255, 255, 255, alpha), (int(p[0]), int(p[1])), int(p[4]))

        card_rect = glass_card()

        # Başlık
        title = title_font.render("Veri Kaydetme İzni", True, (255, 255, 255))
        screen.blit(title, (W // 2 - title.get_width() // 2, card_rect.top + 30))

        # Metin
        body_lines = [
            "Bu oyun verilerinizi güvenli bir şekilde kaydetmek için",
            f"'{SAVE_FOLDER_NAME}' klasörünü Program Files altında oluşturmak isteyecek.",
            "Yönetici izni yoksa veriler LocalAppData altında saklanacaktır.",
            "",
            "Devam etmek istiyor musunuz?"
        ]
        by = card_rect.top + 120
        for ln in body_lines:
            surf = body_font.render(ln, True, (240, 240, 240))
            screen.blit(surf, (W // 2 - surf.get_width() // 2, by))
            by += int(body_font.get_linesize() * 1.1)

        # Butonlar (renk uyumlu)
        mx, my = pygame.mouse.get_pos()
        for rect, color_base, text in [
            (yes_rect, (40, 180, 130), "Evet"),
            (no_rect, (200, 60, 60), "Hayır")
        ]:
            hover = rect.collidepoint((mx, my))
            glow = int(70 * (0.5 + 0.5 * math.sin(t * 3))) if hover else int(15 * abs(math.sin(t * 1.5)))
            col = (
                min(255, color_base[0] + glow),
                min(255, color_base[1] + glow),
                min(255, color_base[2] + glow)
            )
            pygame.draw.rect(screen, col, rect, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255, 20), rect, width=1, border_radius=12)
            label = btn_font.render(text, True, (255, 255, 255))
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

    # Müzik kapat
    pygame.mixer.music.fadeout(800)

    # Hayır derse çık
    if not accepted:
        pygame.quit()
        sys.exit(0)

    # Klasör oluştur
    save_dir = None
    try:
        pf = os.environ.get("PROGRAMFILES") or os.environ.get("ProgramFiles")
        candidate = os.path.join(pf, SAVE_FOLDER_NAME)
        os.makedirs(candidate, exist_ok=True)
        with open(os.path.join(candidate, "._test"), "w") as f:
            f.write("ok")
        os.remove(os.path.join(candidate, "._test"))
        save_dir = candidate
    except Exception:
        local = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
        candidate = os.path.join(local, SAVE_FOLDER_NAME)
        os.makedirs(candidate, exist_ok=True)
        save_dir = candidate

    print(f"[BİLGİ] Oyun verileri şu klasöre kaydedilecek: {save_dir}")
    return save_dir


# ====================================================
# 📁 Kayıt klasörü oluştur
# ====================================================
SAVE_DIR = os.path.join(os.path.expanduser('~'), 'Documents', 'ATAGULDONER')
os.makedirs(SAVE_DIR, exist_ok=True)
# (permission panel skipped in packaged builds; data stored in Documents)


# ---------------------------
# CONFIG
# ---------------------------
GAME_TITLE = "ATAGUL DONER"
SAVE_FILE = "profiles_save.dat"
SCORES_FILE = "scores.list.txt"
ASSETS_DIR = "assets"
FPS = 60

# design base resolution for scaling
BASE_W = 1920
BASE_H = 1080

# ---------------------------
# Logging
# ---------------------------
LOG_FILE = "game_log.txt"
CRASH_FILE = "crash_log.txt"


def log(msg: str) -> None:
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception:
        pass


def crash_log(exc: Exception) -> None:
    try:
        with open(CRASH_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] EXC: {exc}\n")
            traceback.print_exc(file=f)
            f.write("\n\n")
    except Exception:
        pass

# ---------------------------
# Asset helpers
# ---------------------------

def resource_path(rel: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel)


def make_placeholder(size: Tuple[int,int], color: Tuple[int,int,int], text: str) -> pygame.Surface:
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((240,240,240))
    pygame.draw.rect(surf, color, surf.get_rect(), 4)
    try:
        f = pygame.font.SysFont("Arial", 16)
        t = f.render(text, True, color)
        surf.blit(t, t.get_rect(center=surf.get_rect().center))
    except Exception:
        pass
    return surf


def safe_image(path: str, fallback_size=(120,120)) -> pygame.Surface:
    try:
        img = pygame.image.load(path)
        return img.convert_alpha()
    except Exception:
        return make_placeholder(fallback_size, (150,150,150), os.path.basename(path))


def safe_sound(path: str):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        class S:
            def play(self,*a,**k): pass
        return S()

# ---------------------------
# Save / Load
# ---------------------------

def load_profiles() -> Dict[str, Any]:
    p = os.path.join(SAVE_DIR, SAVE_FILE)
    if os.path.exists(p):
        try:
            with open(p, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            log(f"load_profiles error: {e}")
            return {}
    return {}


def save_profiles(profiles: Dict[str, Any]) -> None:
    try:
        with open(os.path.join(SAVE_DIR, SAVE_FILE), "wb") as f:
            pickle.dump(profiles, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        log(f"save_profiles error: {e}")


def append_score(name: str, score: int) -> None:
    try:
        with open(resource_path(SCORES_FILE), "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{name}\t{score}\n")
    except Exception as e:
        log(f"append_score error: {e}")

# ---------------------------
# Input helper (mouse + touch)
# ---------------------------
class InputMgr:
    def __init__(self, screen_size):
        self.w, self.h = screen_size
        self.last_finger = None
    def finger_to_px(self, fx, fy):
        return int(fx*self.w), int(fy*self.h)
    def iter_pointer(self, events):
        for e in events:
            if e.type == pygame.FINGERDOWN:
                p = self.finger_to_px(e.x, e.y)
                self.last_finger = p
                yield 'down', p
            elif e.type == pygame.FINGERUP:
                p = self.finger_to_px(e.x, e.y)
                self.last_finger = p
                yield 'up', p
            elif e.type == pygame.MOUSEBUTTONDOWN and getattr(e, "button", 0) == 1:
                yield 'down', e.pos
            elif e.type == pygame.MOUSEBUTTONUP and getattr(e, "button", 0) == 1:
                yield 'up', e.pos
    def get_pos(self):
        if self.last_finger:
            return self.last_finger
        return pygame.mouse.get_pos()

# ---------------------------
# MAIN GAME
# ---------------------------
def run_game() -> int:
    last_autosave = pygame.time.get_ticks()
    AUTOSAVE_INTERVAL = 30000
    def save_current_profile():
        """Aktif profili kaydet"""
        nonlocal active_profile, profiles, money, happy_total, shop

        if not active_profile:
            print("⚠️ Aktif profil yok")
            return False

        try:
            profiles[active_profile] = {
                "happy": happy_total,
                "money": money,
                "shop": shop.copy()
            }
            save_profiles(profiles)
            print(f"✅ Kaydedildi: {active_profile} | Para: {money} | Mutlu: {happy_total}")
            return True
        except Exception as e:
            print(f"❌ Kayıt hatası: {e}")
            log(f"save_current_profile error: {e}")
            return False
    try:
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            log("mixer init failed")
        info = pygame.display.Info()

        # start fullscreen but allow windowed fallback
        try:
            screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        except Exception:
            screen = pygame.display.set_mode((BASE_W, BASE_H))

        pygame.display.set_caption(GAME_TITLE)
        width, height = screen.get_size()
        clock = pygame.time.Clock()

        # SCALE FACTOR: compute from base design resolution
        scale_x = width / BASE_W
        scale_y = height / BASE_H
        SCALE = min(scale_x, scale_y)
        # clamp so UI not tiny or huge
        SCALE = max(0.6, min(SCALE, 2.5))
        def s(v):
            # scale integers or tuples
            if isinstance(v, (list, tuple)):
                return tuple(int(x * SCALE) for x in v)
            try:
                return int(v * SCALE)
            except Exception:
                return v

        # fonts (scaled)
        try:
            font_big = pygame.font.SysFont("Arial", s(48), bold=True)
            font_mid = pygame.font.SysFont("Arial", s(24))
            font_small = pygame.font.SysFont("Arial", s(18))
            font_xs = pygame.font.SysFont("Arial", s(14))
        except Exception:
            pygame.font.init()
            font_big = pygame.font.SysFont("Arial", s(48), bold=True)
            font_mid = pygame.font.SysFont("Arial", s(24))
            font_small = pygame.font.SysFont("Arial", s(18))
            font_xs = pygame.font.SysFont("Arial", s(14))

        # music
        try:
            music_file = resource_path(os.path.join(ASSETS_DIR, "music1.mp3"))
            if os.path.exists(music_file):
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
            else:
                log(f"music not found: {music_file}")
        except Exception as e:
            log(f"music load error: {e}")

        # assets (including shop.png background)
        assets = {}
        assets['background'] = safe_image(resource_path(f"{ASSETS_DIR}/background.png"), (width,height))
        assets['shop'] = safe_image(resource_path(f"{ASSETS_DIR}/shop.png"), (width,height))  # used for shop & profile
        assets['counter'] = safe_image(resource_path(f"{ASSETS_DIR}/counter.png"), (s(600),s(200)))
        assets['lavash'] = safe_image(resource_path(f"{ASSETS_DIR}/lavash.png"), s((120,120)))
        assets['meat'] = safe_image(resource_path(f"{ASSETS_DIR}/meat.png"), s((100,100)))
        assets['tomato'] = safe_image(resource_path(f"{ASSETS_DIR}/tomato.png"), s((100,100)))
        assets['lettuce'] = safe_image(resource_path(f"{ASSETS_DIR}/lettuce.png"), s((100,100)))
        assets['fries'] = safe_image(resource_path(f"{ASSETS_DIR}/fries.png"), s((100,100)))
        assets['doner'] = safe_image(resource_path(f"{ASSETS_DIR}/doner.png"), s((180,180)))
        # load images for info screen previews (optional)
        assets['info_preview_1'] = safe_image(resource_path(f"{ASSETS_DIR}/preview1.png"), s((400,225)))
        assets['info_preview_2'] = safe_image(resource_path(f"{ASSETS_DIR}/preview2.png"), s((400,225)))
        assets['info_preview_3'] = safe_image(resource_path(f"{ASSETS_DIR}/preview3.png"), s((400,225)))
        cust_imgs = []
        for i in range(1,6):
            cust_imgs.append(safe_image(resource_path(f"{ASSETS_DIR}/customer_{i}.png"), s((160,320))))

        # core sounds
        bell = safe_sound(resource_path(f"{ASSETS_DIR}/bell.mp3"))
        good_snd = safe_sound(resource_path(f"{ASSETS_DIR}/good1.mp3"))  # fallback
        bad_snd = safe_sound(resource_path(f"{ASSETS_DIR}/bad1.mp3"))
        # shop purchase sounds
        olumlu_snd = safe_sound(resource_path(f"{ASSETS_DIR}/olumlu.mp3"))
        olumsuz_snd = safe_sound(resource_path(f"{ASSETS_DIR}/olumsuz.mp3"))
        # öğretici voiceovers (your files)
        lavash_voice = safe_sound(resource_path(f"{ASSETS_DIR}/lavaş.mp3"))
        meat_voice = safe_sound(resource_path(f"{ASSETS_DIR}/et.mp3"))
        tomato_voice = safe_sound(resource_path(f"{ASSETS_DIR}/domates.mp3"))
        dur_voice = safe_sound(resource_path(f"{ASSETS_DIR}/dür.mp3"))
        teslim_voice = safe_sound(resource_path(f"{ASSETS_DIR}/teslim.mp3"))
        # success/fail variations
        good_sounds = [safe_sound(resource_path(f"{ASSETS_DIR}/good{i}.mp3")) for i in (1,2,3)]
        bad_sounds = [safe_sound(resource_path(f"{ASSETS_DIR}/bad{i}.mp3")) for i in (1,2,3)]

        # geometry (scaled)
        counter = pygame.transform.smoothscale(assets['counter'], (width, min(s(240), assets['counter'].get_height())))
        counter_rect = counter.get_rect(bottom=height)
        start_x = s(80)
        y_top = counter_rect.top + s(20)
        BOX = s(100)
        SPACING = s(40)

        ingredient_order = ["wrap", "meat", "tomato", "lettuce", "fries"]
        ingredients = {
            "wrap": pygame.transform.smoothscale(assets['lavash'], (BOX,BOX)),
            "meat": pygame.transform.smoothscale(assets['meat'], (BOX,BOX)),
            "tomato": pygame.transform.smoothscale(assets['tomato'], (BOX,BOX)),
            "lettuce": pygame.transform.smoothscale(assets['lettuce'], (BOX,BOX)),
            "fries": pygame.transform.smoothscale(assets['fries'], (BOX,BOX)),
            "doner": pygame.transform.smoothscale(assets['doner'], (s(160),s(160)))
        }
        ingredient_rects: Dict[str, pygame.Rect] = {}
        for i,name in enumerate(ingredient_order):
            ingredient_rects[name] = pygame.Rect(start_x + i*(BOX+SPACING), y_top, BOX, BOX)

        # durum area and DUR button; moved up 20 px earlier
        durum_area = pygame.Rect(start_x + len(ingredient_order)*(BOX+SPACING) + s(60), y_top, s(180), s(180))
        dur_button = pygame.Rect(durum_area.centerx - s(60) + s(220), durum_area.bottom + s(10) - s(58), s(120), s(50))  # moved up 20 px

        # gameplay state
        customers: List[Any] = []
        base_max_customers = 3
        customer_slots = [s(150), width//2, width-s(150)]
        spawn_min, spawn_max = 4000, 9000

        wrap_placed = False
        durum_done = False
        durum_items: List[str] = []
        dragging = False
        drag_item = None
        drag_img = None
        dragging_doner = False
        doner_rect: Optional[pygame.Rect] = None

        money = 0
        happy_total = 0

        # achievements system (simple)
        ACHIEVEMENTS: Dict[str, Dict[str, Any]] = {
            "bronze_10": {"name": "Bronz Rozet - 10 Mutlu Müşteri", "cond": lambda s: s.get("happy_total",0) >= 10, "unlocked": False},
            "sell_50": {"name": "50 Dürüm Satışı - VIP Açılır", "cond": lambda s: s.get("total_sold",0) >= 50, "unlocked": False},
            "first_win": {"name": "İlk Mutlu Müşteri", "cond": lambda s: s.get("happy_total",0) >= 1, "unlocked": False},
        }
        achievement_popups: List[Dict[str, Any]] = []
        total_sold = 0

        def check_achievements():
            nonlocal ACHIEVEMENTS, achievement_popups
            state = {"happy_total": happy_total, "total_sold": total_sold}
            for key, data in ACHIEVEMENTS.items():
                if not data.get("unlocked", False):
                    try:
                        if data["cond"](state):
                            data["unlocked"] = True
                            achievement_popups.append({"text": data["name"], "start": pygame.time.get_ticks()})
                    except Exception as e:
                        log(f"achievement check error: {e}")

        def draw_achievements():
            # show popups (stacked)
            now = pygame.time.get_ticks()
            for i, p in enumerate(achievement_popups[:]):
                dt = now - p["start"]
                if dt > 3500:
                    try: achievement_popups.remove(p)
                    except ValueError: pass
                    continue
                y = s(120) + i * s(70) - (dt * 0.02)
                alpha = max(0, min(255, int(255 - (dt / 3500.0) * 255)))
                surf = pygame.Surface((s(520), s(56)), pygame.SRCALPHA)
                surf.fill((20,20,20,220))
                txt = font_mid.render("🔔 " + p["text"], True, (255,255,255))
                surf.blit(txt, (s(12), s(8)))
                screen.blit(surf, (width - s(560), y))

        # shop baseline (max_per_feature set to 5)
        shop = {
            "timer_level": 0, "timer_cost": 150,
            "tip_level": 0, "tip_cost": 200, "tip_chance": 0.0, "tip_amount_min":1, "tip_amount_max":10,
            "spawn_level": 0, "spawn_cost": 150, "spawn_chance": 0.0,
            "income_multiplier": 1.0,
            "patience_multiplier": 1.0,
            "maxcust_level": 0,
            "maxcust_cost": 200,
            "time_freeze_uses": 0,
            "gold_meat_chance": 0.0,
            "vip_chance": 0.0,
            "return_chance": 0.0,
            "combo_multiplier": 1.0,
            "daily_bonus_threshold": 10,
            "daily_bonus_amount": 20,
            "mutlu_bonus": 0,
            "quality_level": 0,
            "time_slow_multiplier": 1.0,
            "max_per_feature": 5
        }

        # ---------------------------
        # 40 CUSTOMER-FOCUSED FEATURES
        # ---------------------------
        FEATURES: List[Dict[str, Any]] = []
        def add_feature(fid:int, name:str, desc:str, cost_key:str, level_key:str, base_cost:int, apply_fn):
            FEATURES.append({
                "id": fid, "name": name, "desc": desc,
                "cost_key": cost_key, "level_key": level_key,
                "base_cost": base_cost, "apply_fn": apply_fn
            })

        # helper apply functions for many features
        def apply_vip_chance(lvl):
            shop['vip_chance'] = min(0.5, 0.02 * lvl)
        def apply_patience(lvl):
            shop['patience_multiplier'] = 1.0 + 0.10 * lvl
        def apply_tip_chance(lvl):
            shop['tip_chance'] = min(0.6, 0.05 * lvl)
        def apply_tip_amount(lvl):
            shop['tip_amount_min'] = 1 + lvl
            shop['tip_amount_max'] = 5 + lvl*2
        def apply_return_chance(lvl):
            shop['return_chance'] = min(0.25, 0.01 * lvl)
        def apply_sad_reduce(lvl):
            shop['patience_multiplier'] += 0.02 * lvl
        def apply_rich_customer(lvl):
            shop['rich_chance'] = min(0.1, 0.01 * lvl)
        def apply_gold_meat(lvl):
            shop['gold_meat_chance'] = min(0.15, 0.01 * lvl)
        def apply_vip_multiplier(lvl):
            shop['vip_multiplier'] = 1.0 + 0.5 * lvl
        def apply_combo_bonus(lvl):
            shop['combo_multiplier'] = 1.0 + 0.05 * lvl
        def apply_daily_bonus(lvl):
            shop['daily_bonus_amount'] = 20 + 5*lvl
        def apply_maxcust(lvl):
            shop['maxcust_level'] = lvl
        def apply_spawnchance(lvl):
            shop['spawn_chance'] = min(0.2, 0.01 * lvl)
        def apply_time_slow(lvl):
            shop['time_slow_multiplier'] = 1.0 + 0.02 * lvl
        def apply_guaranteed_tip(lvl):
            shop['guaranteed_tip_level'] = lvl
        def apply_side_income(lvl):
            shop['side_income_level'] = lvl
        def apply_vip_loyalty(lvl):
            shop['vip_loyalty'] = lvl
        def apply_mutluluk_chain(lvl):
            shop['mutlilik_chain_level'] = lvl
        def apply_bahsis_sigortasi(lvl):
            shop['tip_insurance'] = lvl
        def apply_bonus_customer(lvl):
            shop['bonus_customer_level'] = lvl
        def apply_big_tip_chance(lvl):
            shop['big_tip_chance'] = min(0.05, 0.005 * lvl)
        def apply_attraction(lvl):
            shop['attraction_level'] = lvl
        def apply_lucky_day(lvl):
            shop['lucky_day_level'] = lvl

        # Now add 40 features (ids 1..40)
        add_feature(1, "VIP Şansı", "VIP müşteri gelme ihtimalini artırır.", "vip_cost_1", "vip_level_1", 150, apply_vip_chance)
        add_feature(2, "Sabır Artışı", "Müşterilerin bekleme süresini uzatır.", "patience_cost_2", "patience_level_2", 120, apply_patience)
        add_feature(3, "Bahşiş Oranı", "Bahşiş gelme ihtimalini artırır.", "tip_cost_3", "tip_level_3", 130, apply_tip_chance)
        add_feature(4, "Bahşiş Miktarı", "Bahşiş miktarını artırır.", "tipamt_cost_4", "tipamt_level_4", 140, apply_tip_amount)
        add_feature(5, "Sadık Müşteri", "Aynı müşteri tekrar gelebilir.", "return_cost_5", "return_level_5", 160, apply_return_chance)
        add_feature(6, "Sabırsız Azaltıcı", "Sabırsız müşteri oranını azaltır.", "sad_cost_6", "sad_level_6", 100, apply_sad_reduce)
        add_feature(7, "Şikayet Azaltıcı", "Yanlış dürüm sonrası mutsuzluğu azaltır.", "compl_cost_7", "compl_level_7", 110, apply_sad_reduce)
        add_feature(8, "Zengin Müşteri", "Bazı müşteriler daha fazla öder.", "rich_cost_8", "rich_level_8", 200, apply_rich_customer)
        add_feature(9, "Altın Et Şansı", "Altın et müşteriyi ekstra mutlu eder.", "gold_cost_9", "gold_level_9", 180, apply_gold_meat)
        add_feature(10, "Süper Memnuniyet", "Bazı müşteriler 3 kat mutlu olur.", "super_cost_10", "super_level_10", 170, apply_vip_multiplier)
        add_feature(11, "Geri Dönen Müşteri", "Teslim sonrası aynı müşteri geri gelir.", "greturn_cost_11", "greturn_level_11", 150, apply_return_chance)
        add_feature(12, "VIP Mutluluk", "VIP müşteriden +2 mutluluk puanı.", "viphappy_cost_12", "viphappy_level_12", 160, apply_vip_multiplier)
        add_feature(13, "Ekstra Bahşiş", "2. bahşiş alma ihtimalini artırır.", "extratip_cost_13", "extratip_level_13", 140, apply_tip_chance)
        add_feature(14, "Hızlı Hizmet Bonusu", "Erken teslim ekstra bahşiş verir.", "fast_cost_14", "fast_level_14", 120, apply_big_tip_chance)
        add_feature(15, "Şöhret Artışı", "Mutlu müşteri oranı artarsa daha fazla müşteri gelir.", "rep_cost_15", "rep_level_15", 200, apply_attraction)
        add_feature(16, "Müşteri Hızı Düşüşü", "Müşteri süreleri yavaşlar.", "slow_cost_16", "slow_level_16", 110, apply_time_slow)
        add_feature(17, "Karmaşık Sipariş", "Müşteriler daha karmaşık dürüm ister (çeşitlilik).", "comb_cost_17", "comb_level_17", 130, apply_combo_bonus)
        add_feature(18, "Sakin Kalma", "Sabırsız müşteriler daha sakin olur.", "calm_cost_18", "calm_level_18", 115, apply_patience)
        add_feature(19, "Çift VIP", "Arka arkaya VIP gelme ihtimalini artırır.", "dvip_cost_19", "dvip_level_19", 220, apply_vip_chance)
        add_feature(20, "Bahşiş Sigortası", "Yanlış dürümde bahşişin %50’si korunur.", "ins_cost_20", "ins_level_20", 190, apply_bahsis_sigortasi)
        add_feature(21, "VIP Bahşiş Katlayıcı", "VIP müşteriler 2 kat bahşiş verir.", "viptip_cost_21", "viptip_level_21", 210, apply_vip_multiplier)
        add_feature(22, "Sabır Sigortası", "Süre bittiğinde müşteri hemen gitmez.", "psig_cost_22", "psig_level_22", 150, apply_patience)
        add_feature(23, "Süper Sadakat", "Sadık müşteriler VIP olabilir.", "sloyal_cost_23", "sloyal_level_23", 220, apply_vip_loyalty)
        add_feature(24, "Müşteri Önerisi", "Mutlu müşteri 1 yeni müşteri getirir.", "ref_cost_24", "ref_level_24", 170, apply_bonus_customer)
        add_feature(25, "Güleryüz Bonus", "Dürüm teslim sonrası +1 sabır.", "smile_cost_25", "smile_level_25", 90, apply_patience)
        add_feature(26, "VIP Combo", "2 VIP arka arkaya ekstra bonus.", "vipcombo_cost_26", "vipcombo_level_26", 230, apply_combo_bonus)
        add_feature(27, "Şikayet Yok", "Mutsuz müşteri sistemi daha toleranslı.", "nocompl_cost_27", "nocompl_level_27", 140, apply_sad_reduce)
        add_feature(28, "Zaman Dondurucu Şansı", "Teslim sonrası zaman geçici durur.", "freeze_cost_28", "freeze_level_28", 240, apply_time_slow)
        add_feature(29, "Bahşiş Patlaması", "10 müşteriden biri çok büyük bahşiş verir.", "burst_cost_29", "burst_level_29", 300, apply_big_tip_chance)
        add_feature(30, "Geri Çağırma", "Giden müşteri tekrar çağrılabilir.", "recall_cost_30", "recall_level_30", 160, apply_return_chance)
        add_feature(31, "VIP Sadakati", "VIP müşteriler genelde bahşiş bırakır.", "vipsad_cost_31", "vipsad_level_31", 200, apply_vip_loyalty)
        add_feature(32, "Mutluluk Zinciri", "Art arda 3 doğru dürüm bonus getirir.", "chain_cost_32", "chain_level_32", 180, apply_mutluluk_chain)
        add_feature(33, "Hatalı Dürüm Affı", "1 hatalı dürüm sonrası müşteri affeder.", "forgive_cost_33", "forgive_level_33", 150, apply_sad_reduce)
        add_feature(34, "Müşteri Çekimi", "Müşteri çıkma aralığı azalır (daha sık gelir).", "pull_cost_34", "pull_level_34", 210, apply_attraction)
        add_feature(35, "Günlük Sadakat", "Oyun tekrar açıldığında ekstra müşteri gelir.", "daily_cost_35", "daily_level_35", 170, apply_daily_bonus)
        add_feature(36, "Bahşiş Yağmuru", "30 sn boyunca bahşişler iki kat olur.", "rain_cost_36", "rain_level_36", 260, apply_big_tip_chance)
        add_feature(37, "Sabır Dondurucu", "Müşteri süreleri kısa süre durur.", "pause_cost_37", "pause_level_37", 200, apply_time_slow)
        add_feature(38, "Şanslı Gün", "Oyun başında tüm oranlar %10 artar.", "lucky_cost_38", "lucky_level_38", 180, apply_lucky_day)
        add_feature(39, "Memnuniyet Zinciri", "5 mutlu müşteri sonrası bonus gelir.", "mchain_cost_39", "mchain_level_39", 220, apply_mutluluk_chain)
        add_feature(40, "Geri Bildirim Şansı", "Mutlu müşteriler +1 sadakat kazandırır.", "fb_cost_40", "fb_level_40", 140, apply_bonus_customer)

        # ensure shop keys exist for all features
        for feat in FEATURES:
            shop.setdefault(feat["cost_key"], feat["base_cost"])
            shop.setdefault(feat["level_key"], 0)

        # trackers and other globals
        tip_messages: List[Dict[str, Any]] = []
        daily_counter = 0
        combo_count = 0
        combo_last_time = 0
        last_spawn = pygame.time.get_ticks()
        time_freeze_active_until = 0
        auto_prep_active_until = 0
        last_key_press_times: Dict[str, int] = {}
        DEBOUNCE_MS = 250

        input_mgr = InputMgr((width,height))
        profiles = load_profiles()
        active_profile = None

        # ---------------------------
        # Utility: fade in/out transitions
        # ---------------------------
        def fade_out(duration_ms=400):
            start = pygame.time.get_ticks()
            overlay = pygame.Surface((width, height))
            clock_local = pygame.time.Clock()
            while True:
                t = pygame.time.get_ticks() - start
                a = min(255, int((t / duration_ms) * 255))
                overlay.fill((0,0,0))
                overlay.set_alpha(a)
                screen.blit(overlay, (0,0))
                pygame.display.flip()
                if t >= duration_ms:
                    break
                clock_local.tick(FPS)

        def fade_in(duration_ms=400):
            start = pygame.time.get_ticks()
            overlay = pygame.Surface((width, height))
            clock_local = pygame.time.Clock()
            while True:
                t = pygame.time.get_ticks() - start
                a = max(0, 255 - int((t / duration_ms) * 255))
                overlay.fill((0,0,0))
                overlay.set_alpha(a)
                screen.blit(overlay, (0,0))
                pygame.display.flip()
                if t >= duration_ms:
                    break
                clock_local.tick(FPS)

        # ---------------------------
        # Animated gradient background for menus
        # ---------------------------
        gradient_phase = 0.0
        def draw_animated_gradient():
            nonlocal gradient_phase
            # simple slow color cycle
            gradient_phase += 0.0008
            if gradient_phase > 1.0:
                gradient_phase -= 1.0
            # compute two colors
            def lerp(a,b,t):
                return int(a+(b-a)*t)
            # color A cycles through warm palette, color B cycles through cool palette
            ca = (lerp(18,200,(gradient_phase)%1.0), lerp(18,90,(gradient_phase+0.2)%1.0), lerp(22,120,(gradient_phase+0.4)%1.0))
            cb = (lerp(40,10,(gradient_phase+0.6)%1.0), lerp(40,20,(gradient_phase+0.8)%1.0), lerp(60,200,(gradient_phase+0.1)%1.0))
            # vertical gradient
            surface = pygame.Surface((width, height))
            for y in range(0, height, 6):
                t = y / height
                r = int(ca[0] * (1-t) + cb[0] * t)
                g = int(ca[1] * (1-t) + cb[1] * t)
                b = int(ca[2] * (1-t) + cb[2] * t)
                pygame.draw.rect(surface, (r,g,b), (0, y, width, 6))
            # slight overlay of shop.png faded for depth
            try:
                shop_scaled = pygame.transform.smoothscale(assets['shop'], (width, height))
                shop_scaled.set_alpha(40)
                surface.blit(shop_scaled, (0,0))
            except Exception:
                pass
            screen.blit(surface, (0,0))

        # ---------------------------
        #  Mode selection screen
        # ---------------------------
        def mode_select_screen():
            # returns mode string: "ISINMA MEKANI - KAYIT YOK"
            options = ["ISINMA MEKANI - KAYIT YOK"]
            selected = 0
            running = True
            btn_w = s(420); btn_h = s(84); spacing = s(22)
            while running:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        return None
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_ESCAPE:
                            return None
                        if ev.key in (pygame.K_LEFT, pygame.K_a):
                            selected = max(0, selected-1)
                        if ev.key in (pygame.K_RIGHT, pygame.K_d):
                            selected = min(len(options)-1, selected+1)
                        if ev.key == pygame.K_RETURN:
                            return options[selected]
                    if ev.type == pygame.MOUSEBUTTONDOWN and getattr(ev,"button",0)==1:
                        mx,my = ev.pos
                        bx = width//2 - btn_w//2
                        by = s(280)
                        for i,opt in enumerate(options):
                            rect = pygame.Rect(bx, by + i*(btn_h+spacing), btn_w, btn_h)
                            if rect.collidepoint((mx,my)):
                                return opt
                # draw
                draw_animated_gradient()
                title = font_big.render("Oyun Modu Seç", True, (255,255,255))
                screen.blit(title, (width//2 - title.get_width()//2, s(80)))
                bx = width//2 - btn_w//2
                by = s(260)
                for i,opt in enumerate(options):
                    rect = pygame.Rect(bx, by + i*(btn_h+spacing), btn_w, btn_h)
                    color = (60,160,80) if i==selected else (40,40,60)
                    pygame.draw.rect(screen, color, rect, border_radius=s(12))
                    txt = font_mid.render(opt, True, (255,255,255))
                    screen.blit(txt, txt.get_rect(center=rect.center))
                    # description
                    desc = ""
                    if opt == "ISINMA MEKANI - KAYIT YAPILMAZ":
                        desc = "Normal oyun. Skor toplama."
                    elif opt == "Süre Savaşı":
                        desc = "60 saniyede en çok mutlu müşteri."
                    else:
                        desc = "      KAYIT YAPILMAZ ISINMA İÇİN BİREBİR"
                    ds = font_small.render(desc, True, (220,220,220))
                    screen.blit(ds, (rect.x + s(18), rect.y + rect.h + s(8)))
                hint = font_small.render("ESC: Geri | ←/→ seç | ENTER: Başlat", True, (200,200,200))
                screen.blit(hint, (width//2 - hint.get_width()//2, height - s(60)))
                pygame.display.flip()
                clock.tick(FPS)

        # OYNA screen preserved (touch support)
        def profile_screen():
            nonlocal active_profile, money, happy_total, shop, profiles
            names = list(profiles.keys())
            selected = 0 if names else -1
            typing = False
            text_in = ""
            # On-screen simple buttons for touch: choose name or tap create
            while True:
                # use shop as background per your request
                try:
                    screen.blit(pygame.transform.smoothscale(assets['shop'], (width, height)), (0,0))
                except:
                    screen.fill((20,20,30))
                title = font_big.render("PROFIL SEÇ / OLUŞTUR", True, (255,255,255))
                screen.blit(title, (width//2 - title.get_width()//2, s(40)))
                # draw name list as buttons
                box_x = width//4
                box_y = s(160)
                button_h = s(40)
                name_rects = []
                for i,n in enumerate(names):
                    rect = pygame.Rect(box_x - s(160), box_y + i*(button_h+s(8)), s(320), button_h)
                    name_rects.append((rect,n))
                    color = (80,80,120) if i!=selected else (120,100,60)
                    pygame.draw.rect(screen, color, rect, border_radius=8)
                    t = font_mid.render(n, True, (255,255,255))
                    screen.blit(t, (rect.centerx - t.get_width()//2, rect.centery - t.get_height()//2))
                # new profile box
                input_box = pygame.Rect(width//2 - s(210), s(160), s(420), s(36))
                pygame.draw.rect(screen, (50,50,60), input_box, border_radius=6)
                lbl = font_small.render("Profil adı:", True, (200,200,200))
                screen.blit(lbl, (input_box.x+s(8), input_box.y+s(6)))
                name_disp = font_mid.render(text_in if typing else ("Yeni profil" if not names else ""), True, (255,255,255))
                screen.blit(name_disp, (input_box.x+s(140), input_box.y+s(2)))
                hint = font_small.render("M tuşu: Mağazayı açar | Dokunarak seç / kutuya dokunarak yaz", True, (160,160,160))
                screen.blit(hint, (width//2 - hint.get_width()//2, height-s(60)))
                pygame.display.flip()

                evs = pygame.event.get()
                for ev in evs:
                    if ev.type == pygame.QUIT:
                        save_current_profile()  # ✅ EKLE
                        append_score(active_profile or "Guest", happy_total)
                        return 0
                        pygame.quit(); sys.exit()
                    if ev.type == pygame.FINGERDOWN:
                        px,py = int(ev.x*width), int(ev.y*height)
                        # check name buttons
                        for rect,name in name_rects:
                            if rect.collidepoint((px,py)):
                                active_profile = name
                                data = profiles[active_profile]
                                happy_total = data.get("happy",0)
                                money = data.get("money",0)
                                shop.update(data.get("shop", shop))
                                return
                        if input_box.collidepoint((px,py)):
                            typing = True
                            text_in = ""
                    if ev.type == pygame.MOUSEBUTTONDOWN and getattr(ev,"button",0)==1:
                        mx,my = ev.pos
                        # select name
                        for rect,name in name_rects:
                            if rect.collidepoint((mx,my)):
                                active_profile = name
                                data = profiles[active_profile]
                                happy_total = data.get("happy",0)
                                money = data.get("money",0)
                                shop.update(data.get("shop", shop))
                                return
                        if input_box.collidepoint((mx,my)):
                            typing = True
                            text_in = ""
                    if ev.type == pygame.KEYDOWN:
                        if typing:
                            if ev.key == pygame.K_RETURN:
                                if text_in.strip():
                                    n = text_in.strip()
                                    if n not in profiles:
                                        profiles[n] = {"happy":0,"money":0,"shop":shop.copy()}
                                    active_profile = n
                                    data = profiles[n]
                                    happy_total = data.get("happy",0)
                                    money = data.get("money",0)
                                    shop.update(data.get("shop", shop))
                                    save_profiles(profiles)
                                    return
                                typing = False
                            elif ev.key == pygame.K_BACKSPACE:
                                text_in = text_in[:-1]
                            else:
                                ch = ev.unicode
                                text_in += ch
                        else:
                            if ev.key == pygame.K_ESCAPE:
                                # Kaydet
                                if active_profile:
                                    profiles[active_profile] = {
                                        "happy": happy_total,
                                        "money": money,
                                        "shop": shop.copy()
                                    }
                                    save_profiles(profiles)
                                    print(f"✅ ESC - Profil kaydedildi: {active_profile}")

                                # Eğer profil yoksa ilk profili seç
                                if not active_profile and names:
                                    active_profile = names[0]
                                    data = profiles[active_profile]
                                    happy_total = data.get("happy", 0)
                                    money = data.get("money", 0)
                                    shop.update(data.get("shop", shop))
                                    print(f"✅ İlk profil yüklendi: {active_profile}")

                                return
                clock.tick(FPS)

        # ---------------------------
        # BİLGİ screen with scrollable guide + image previews
        # ---------------------------
        def info_screen():
            # vertical scroll
            scroll = 0
            max_scroll = s(1200)
            running = True
            while running:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        return
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_ESCAPE:
                            return
                        if ev.key == pygame.K_PAGEUP:
                            scroll = max(0, scroll - s(200))
                        if ev.key == pygame.K_PAGEDOWN:
                            scroll = min(max_scroll, scroll + s(200))
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if ev.button == 4:  # wheel up
                            scroll = max(0, scroll - s(60))
                        if ev.button == 5:  # wheel down
                            scroll = min(max_scroll, scroll + s(60))
                # draw background
                draw_animated_gradient()
                title = font_big.render("Oyun Info & Rehber", True, (255,255,255))
                screen.blit(title, (s(60), s(40) - scroll))
                # guide text (multi-paragraph)
                lines = [
                    "ATAGUL DONER Oyun Rehberi",
                    "İLETİŞİM: atagul.games@gmail.com",
                    "YAPIMCI: AHMET METE - ATAGUL GAMES",
                    "Oyun Hedefi:",
                    "- Müşterilere doğru dürümleri vererek mutlu müşteri puanı kazan.",
                    "- Mağazadan güçlendirmeler alarak daha fazla müşteri çek.",
                    "",
                    "Kontroller:",
                    "- Fare veya dokunma ile malzemeyi sürükleyin.",
                    "- 'DÜR' butonuna basarak dürümü tamamlayın.",
                    "- M: Mağaza | T: Zaman dondurucu",
                    "",
                    "Oyun Modları:",
                    "- ISINMA MEKANI: Kayıtsız , ısınmak için birebir",
                    "- Time Attack: 60 saniyede en çok mutlu müşteri topla. (YAKINDA)",
                    "",
                    "İpuçları:",
                    "- Kombolar bonus getirir.",
                    "- VIP müşterilere dikkat edin; ekstra ödül verirler.",
                    "",
                    "Mağaza özellikleri ve açıklamaları aşağıdadır. (Mağazada toplam 40 özellik bulunur.)",
                    "",
                    "- 1) VIP Şansı: VIP müşteri gelme ihtimalini artırır.",
                    "- 2) Sabır Artışı: Müşterilerin bekleme süresini uzatır.",
                    "- 3) Bahşiş Oranı: Bahşiş gelme ihtimalini artırır.",
                    "- 4) Bahşiş Miktarı: Bahşiş miktarını artırır.",
                    "- 5) Sadık Müşteri: Aynı müşteri tekrar gelebilir.",
                    "- 6) Sabırsız Azaltıcı: Sabırsız müşteri oranını düşürür.",
                    "- 7) Şikayet Azaltıcı: Yanlış dürüm sonrası mutsuzluğu azaltır.",
                    "- 8) Zengin Müşteri: Bazı müşteriler daha fazla ödeme yapar.",
                    "- 9) Altın Et Şansı: Altın et → ekstra mutlu müşteri.",
                    "- 10) Süper Memnuniyet: Bazı müşteriler 3 kat mutlu olur.",
                    "- 11) Geri Dönen Müşteri: Teslim sonrası tekrar gelebilir.",
                    "- 12) VIP Mutluluk: VIP müşteriden +2 mutluluk puanı gelir.",
                    "- 13) Ekstra Bahşiş: Birden fazla bahşiş alma ihtimali.",
                    "- 14) Hızlı Hizmet Bonusu: Erken teslim → ekstra bahşiş.",
                    "- 15) Şöhret Artışı: Mutlu müşteri → daha fazla müşteri getirir.",
                    "- 16) Müşteri Hızı Düşüşü: Süre yavaş akar.",
                    "- 17) Karmaşık Sipariş: Daha farklı dürüm istekleri gelir.",
                    "- 18) Sakin Kalma: Sabırsız müşteriler daha geç sinirlenir.",
                    "- 19) Çift VIP: Arka arkaya VIP gelme ihtimali.",
                    "- 20) Bahşiş Sigortası: Yanlış dürümde bahşişin %50'si korunur.",
                    "- 21) VIP Bahşiş Katlayıcı: VIP → 2 kat bahşiş verir.",
                    "- 22) Sabır Sigortası: Süre bitince müşteri hemen gitmez.",
                    "- 23) Süper Sadakat: Sadık müşteri VIP olabilir.",
                    "- 24) Müşteri Önerisi: Mutlu müşteri yeni müşteri getirir.",
                    "- 25) Güleryüz Bonusu: Teslim sonrası sabır kazanılır.",
                    "- 26) VIP Combo: 2 VIP arka arkaya → bonus.",
                    "- 27) Şikayet Yok: Müşteri toleransı artar.",
                    "- 28) Zaman Dondurucu Şansı: Dürüm sonrası süre donar.",
                    "- 29) Bahşiş Patlaması: 10 müşteriden biri büyük bahşiş verir.",
                    "- 30) Geri Çağırma: Giden müşteri geri çağrılır.",
                    "- 31) VIP Sadakati: VIP → mutlaka bahşiş bırakır.",
                    "- 32) Mutluluk Zinciri: 3 doğru dürüm → bonus.",
                    "- 33) Hatalı Dürüm Affı: Yanlış dürüm affedilir.",
                    "- 34) Müşteri Çekimi: Müşteri çıkma aralığı azalır.",
                    "- 35) Günlük Sadakat: Her açışta ekstra müşteri gelir.",
                    "- 36) Bahşiş Yağmuru: 30 saniyeliğine bahşişler 2 kat.",
                    "- 37) Sabır Dondurucu: Süre kısa süre durur.",
                    "- 38) Şanslı Gün: Oyun başında tüm oranlar +%10.",
                    "- 39) Memnuniyet Zinciri: 5 mutlu müşteri → bonus.",
                    "- 40) Geri Bildirim Şansı: Mutlu müşteri +1 sadakat kazandırır.",
                    ""
                ]

                y = s(120) - scroll
                for ln in lines:
                    txt = font_small.render(ln, True, (240,240,240))
                    screen.blit(txt, (s(80), y))
                    y += s(28)
                # image previews horizontally
                px = s(80)
                py = y + s(12)
                for key in ('','',''):
                    img = assets.get(key)
                    if img:
                        iw = img.get_width()
                        ih = img.get_height()
                        screen.blit(img, (px, py))
                        px += iw + s(20)
                # hint
                hint = font_small.render("                                                                                                                                                                                                                                                                              ESC: Geri | Mouse wheel veya PageUp/PageDown ile kaydır", True, (200,200,200))
                screen.blit(hint, (s(60), height - s(60)))
                pygame.display.flip()
                clock.tick(FPS)

        # ---------------------------
        # Main menu to improve navigation (now with animated bg + fade + BİLGİ + MODE)
        # ---------------------------
        def main_menu():
            menu_running = True
            selected = 0
            options = ["MODLAR", "BİLGİ", "OYNA", "ÇIKIŞ"]
            btn_w = s(480)
            btn_h = s(84)
            spacing = s(28)
            # add logo animation simple (scale pulsing)
            logo_base = font_big.render(GAME_TITLE, True, (255,255,255))
            logo_pulse = 0.0
            last_pulse = pygame.time.get_ticks()
            while menu_running:
                try:
                    # background animated
                    draw_animated_gradient()
                except:
                    screen.fill((18,18,22))
                # logo pulse
                logo_pulse += 0.02
                pulse_scale = 1.0 + 0.03 * (1.0 + math_sin(logo_pulse))
                try:
                    # scaled logo
                    lg = pygame.transform.rotozoom(logo_base, 0, pulse_scale)
                    screen.blit(lg, (width//2 - lg.get_width()//2, s(40)))
                except Exception:
                    title = font_big.render(GAME_TITLE, True, (255,255,255))
                    screen.blit(title, (width//2 - title.get_width()//2, s(40)))
                # draw buttons
                bx = width//2 - btn_w//2
                by = s(260)
                for i,opt in enumerate(options):
                    rect = pygame.Rect(bx, by + i*(btn_h+spacing), btn_w, btn_h)
                    color = (80,140,60) if i==selected else (40,40,60)
                    pygame.draw.rect(screen, color, rect, border_radius=s(12))
                    txt = font_mid.render(opt, True, (255,255,255))
                    screen.blit(txt, txt.get_rect(center=rect.center))
                hint = font_small.render("Yukarı/Aşağı: Seç | ENTER: Onay | Dokunma destekli", True, (200,200,200))
                screen.blit(hint, (width//2 - hint.get_width()//2, height - s(60)))
                pygame.display.flip()

                evs = pygame.event.get()
                for ev in evs:
                    if ev.type == pygame.QUIT:
                        return "ÇIKIŞ"
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_ESCAPE:
                            return "ÇIKIŞ"
                        if ev.key in (pygame.K_LEFT, pygame.K_a):
                            selected = max(0, selected-1)
                        if ev.key in (pygame.K_RIGHT, pygame.K_d):
                            selected = min(len(options)-1, selected+1)
                        if ev.key == pygame.K_RETURN:
                            # fade out menu -> action -> fade in
                            choice = options[selected]
                            fade_out(300)
                            if choice == "MODLAR":
                                # mode select
                                mode = mode_select_screen()
                                fade_in(300)
                                return "MODLAR:" + (mode or "Klasik")
                            elif choice == "BİLGİ":
                                info_screen()
                                fade_in(300)
                                break
                            elif choice == "OYNA":
                                profile_screen()
                                fade_in(300)
                                return "OYNA"
                            elif choice == "ÇIKIŞ":
                                return "ÇIKIŞ"
                    if ev.type == pygame.FINGERDOWN:
                        px,py = int(ev.x*width), int(ev.y*height)
                        for i in range(len(options)):
                            rect = pygame.Rect(bx, by + i*(btn_h+spacing), btn_w, btn_h)
                            if rect.collidepoint((px,py)):
                                choice = options[i]
                                fade_out(300)
                                if choice == "MODLAR":
                                    mode = mode_select_screen()
                                    fade_in(300)
                                    return "MODLAR:" + (mode or "Klasik")
                                elif choice == "BİLGİ":
                                    info_screen()
                                    fade_in(300)
                                    break
                                elif choice == "OYNA":
                                    profile_screen()
                                    fade_in(300)
                                    return "OYNA"
                                elif choice == "ÇIKIŞ":
                                    return "ÇIKIŞ"
                    if ev.type == pygame.MOUSEBUTTONDOWN and getattr(ev, 'button', 0)==1:
                        mx,my = ev.pos
                        for i in range(len(options)):
                            rect = pygame.Rect(bx, by + i*(btn_h+spacing), btn_w, btn_h)
                            if rect.collidepoint((mx,my)):
                                choice = options[i]
                                fade_out(300)
                                if choice == "MODLAR":
                                    mode = mode_select_screen()
                                    fade_in(300)
                                    return "MODLAR:" + (mode or "Klasik")
                                elif choice == "BİLGİ":
                                    info_screen()
                                    fade_in(300)
                                    break
                                elif choice == ("OYNA"):
                                    profile_screen()
                                    fade_in(300)
                                    return "OYNA"
                                elif choice == "ÇIKIŞ":
                                    return "ÇIKIŞ"
                clock.tick(FPS)

        # small helper math sin without extra import
        import math
        def math_sin(x):
            return math.sin(x)

        # run main menu first to improve navigation
        choice = main_menu()
        if choice == "ÇIKIŞ":
            pygame.quit(); return 0
        # handle shop/profile flow
        if choice == "OYNA":
            profile_screen()
            # after profile, fallthrough to shop screen pause
            # call shop screen later in loop
        mode = "ISINMA MEKANI - KAYIT YAPILMAZ"
        if choice and choice.startswith("MODLAR:"):
            _, msel = choice.split(":",1)
            if msel:
                mode = msel

        if choice == "OYNA":
            # already handled
            pass

        # Öğretici state machine (will run once)
        öğretici_active = True
        öğretici_step = 0
        öğretici_steps_text = [
            "Lavash'ı al ve dürüm alanına sürükle.",
            "Şimdi eti al ve dürüm alanına sürükle.",
            "Şimdi domatesi al ve dürüm alanına sürükle.",
            "DÜR butonuna bas ve dürümü yap.",
            "Dürümü müşteriye ver."
        ]
        öğretici_voices = [lavash_voice, meat_voice, tomato_voice, dur_voice, teslim_voice]
        try:
            öğretici_voices[0].play()
        except:
            pass

        def play_random_good():
            try:
                s = random.choice(good_sounds)
                s.play()
            except:
                try:
                    good_snd.play()
                except:
                    pass

        def play_random_bad():
            try:
                s = random.choice(bad_sounds)
                s.play()
            except:
                try:
                    bad_snd.play()
                except:
                    pass

        # Customer for öğretici: will request meat+tomato
        class CustomerÖğretici:
            def __init__(self, img: pygame.Surface, pos_x: int):
                self.img = img
                self.rect = img.get_rect(midbottom=(pos_x, counter_rect.top))
                self.order = ["meat","tomato"]
                self.dialog = "Et ve domatesli dürüm istiyorum."
            def draw(self):
                screen.blit(self.img, self.rect)
                try:
                    d_s = font_small.render(self.dialog, True, (255,255,255))
                    db = pygame.Surface((d_s.get_width()+s(10), d_s.get_height()+s(8)), pygame.SRCALPHA)
                    db.fill((0,0,0,180))
                    db.blit(d_s, (s(5),s(4)))
                    screen.blit(db, (self.rect.left, self.rect.top - s(80)))
                except Exception:
                    pass

        öğretici_customer = CustomerÖğretici(cust_imgs[0], width//2 - s(200))

        def draw_ingredients_with_highlight(active_name: Optional[str]):
            for name, rect in ingredient_rects.items():
                img = ingredients[name]
                if active_name is None:
                    screen.blit(img, rect)
                else:
                    if name == active_name:
                        screen.blit(img, rect)
                        pygame.draw.rect(screen, (255,200,0), rect, s(3), border_radius=6)
                    else:
                        surf = img.copy()
                        dark = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
                        dark.fill((0,0,0,180))
                        surf.blit(dark, (0,0))
                        screen.blit(surf, rect)

        def öğretici_place_check(item_name: str):
            nonlocal öğretici_step, öğretici_active
            if öğretici_step == 0 and item_name == "wrap":
                öğretici_step = 1
                try: öğretici_voices[1].play()
                except: pass
                return True
            if öğretici_step == 1 and item_name == "meat":
                öğretici_step = 2
                try: öğretici_voices[2].play()
                except: pass
                return True
            if öğretici_step == 2 and item_name == "tomato":
                öğretici_step = 3
                try: öğretici_voices[3].play()
                except: pass
                return True
            return False

        class Customer:
            def __init__(self, img: pygame.Surface, pos_x: int, base_timer:int, vip=False):
                self.img = img
                self.rect = img.get_rect(midbottom=(pos_x, counter_rect.top))
                self.wants_lettuce = random.choice([True, False])
                self.is_vip = vip
                choices = [
                    ["meat"],
                    ["meat", "tomato"],
                    ["meat", "fries"],
                    ["meat", "tomato", "fries"]
                ]
                order = random.choice(choices)
                if self.wants_lettuce:
                    if "lettuce" not in order:
                        order.append("lettuce")
                else:
                    if "lettuce" in order:
                        order.remove("lettuce")
                # more complex orders if shop encourages
                if shop.get('comb_level_17',0) > 0 and random.random() < min(0.25, 0.05 * shop.get('comb_level_17',0)):
                    # add extra random ingredient
                    extra = random.choice(["fries","tomato","meat"])
                    if extra not in order:
                        order.append(extra)
                self.order = order
                self.dialog = "Marul " + ("olsun" if self.wants_lettuce else "olmasın")
                if self.is_vip:
                    self.dialog = "[VIP] " + self.dialog
                pat_mult = shop.get("patience_multiplier", 1.0)
                self.timer = int(base_timer * pat_mult * shop.get("time_slow_multiplier",1.0))
                self.start = pygame.time.get_ticks()
            def draw(self):
                screen.blit(self.img, self.rect)
                try:
                    txt = ", ".join(self.order)
                    surf_t = font_xs.render(txt, True, (0,0,0))
                    box = pygame.Surface((surf_t.get_width()+s(16), surf_t.get_height()+s(12)), pygame.SRCALPHA)
                    box.fill((255,255,255,230))
                    pygame.draw.rect(box, (0,0,0), box.get_rect(), 2)
                    box.blit(surf_t, (s(8),s(6)))
                    screen.blit(box, (self.rect.centerx - box.get_width()//2, self.rect.top - s(46)))
                except Exception:
                    pass
                rem = max(0, self.timer - (pygame.time.get_ticks() - self.start))//1000
                time_box = pygame.Rect(self.rect.right+s(8), self.rect.top+s(8), s(42), s(36))
                pygame.draw.rect(screen, (255,255,0), time_box)
                time_txt = font_small.render(str(rem), True, (0,0,0))
                screen.blit(time_txt, time_txt.get_rect(center=time_box.center))
                try:
                    d_s = font_small.render(self.dialog, True, (255,255,255))
                    db = pygame.Surface((d_s.get_width()+s(10), d_s.get_height()+s(8)), pygame.SRCALPHA)
                    db.fill((0,0,0,180))
                    db.blit(d_s, (s(5),s(4)))
                    screen.blit(db, (self.rect.left, self.rect.top - s(80)))
                except Exception:
                    pass

        base_customer_timer = 15000

        def play_success():
            play_random_good()

        def play_fail():
            play_random_bad()

        # shop_screen_pause - extended to show 40 features
        def shop_screen_pause():
            nonlocal money, shop, active_profile, profiles, happy_total, customers, last_spawn
            pause_start = pygame.time.get_ticks()
            page = 0
            total_features = len(FEATURES)
            per_page = 12
            total_pages = (total_features + per_page - 1) // per_page
            running_shop = True
            show_confirm = False

            cols = 3; rows = 4
            grid_w = min(width - s(160), cols * s(360) + (cols-1)*s(16))
            grid_h = min(height - s(240), rows * s(120) + (rows-1)*s(12))
            btn_w = grid_w // cols - s(12)
            btn_h = grid_h // rows - s(8)
            grid_x = (width - (btn_w*cols + s(12)*(cols-1)))//2
            grid_y = s(140)

            left_rect = pygame.Rect(s(40), height//2 - s(36), s(64), s(72))
            right_rect = pygame.Rect(width-s(104), height//2 - s(36), s(64), s(72))
            back_rect = pygame.Rect(width//2 - s(80), height - s(110), s(160), s(56))

            while running_shop:
                try:
                    screen.blit(pygame.transform.smoothscale(assets['shop'], (width, height)), (0,0))
                except Exception:
                    screen.fill((8,8,16))

                title = font_big.render("MAĞAZA", True, (255,255,255))
                screen.blit(title, (width//2 - title.get_width()//2, s(24)))
                info = font_small.render(f"Para: ₺{money}", True, (255,220,50))
                screen.blit(info, (width//2 - info.get_width()//2, s(88)))

                start_index = page * per_page
                for idx in range(per_page):
                    feat_idx = start_index + idx
                    col = idx % cols
                    row = idx // cols
                    x = grid_x + col * (btn_w + s(12))
                    y = grid_y + row * (btn_h + s(12))
                    rect = pygame.Rect(x, y, btn_w, btn_h)
                    if feat_idx < total_features:
                        feat = FEATURES[feat_idx]
                        lvlk = feat["level_key"]
                        lvl = shop.get(lvk := lvlk, 0)
                        costk = feat["cost_key"]
                        cost = shop.get(costk, feat["base_cost"])
                        if lvl >= shop["max_per_feature"]:
                            pygame.draw.rect(screen, (80,80,90), rect, border_radius=10)
                            name_surf = font_small.render(f"{feat['id']}. {feat['name']}", True, (180,180,180))
                            screen.blit(name_surf, (rect.x+s(10), rect.y+s(8)))
                            lvl_surf = font_xs.render(f"Lv {lvl}/{shop['max_per_feature']}", True, (160,160,160))
                            screen.blit(lvl_surf, (rect.x+s(10), rect.y+s(36)))
                            cost_surf = font_xs.render("MAKS", True, (160,160,160))
                            screen.blit(cost_surf, (rect.right - cost_surf.get_width() - s(10), rect.y+s(8)))
                            pygame.draw.line(screen, (140,140,140), (rect.x+s(8), rect.centery), (rect.right-s(8), rect.centery), s(3))
                        else:
                            pygame.draw.rect(screen, (50,130,200), rect, border_radius=10)
                            name_surf = font_small.render(f"{feat['id']}. {feat['name']}", True, (255,255,255))
                            screen.blit(name_surf, (rect.x+s(10), rect.y+s(8)))
                            desc_surf = font_xs.render(feat['desc'], True, (230,230,230))
                            screen.blit(desc_surf, (rect.x+s(10), rect.y+s(34)))
                            lvl_surf = font_xs.render(f"Lv {lvl}/{shop['max_per_feature']}", True, (240,240,240))
                            screen.blit(lvl_surf, (rect.x+s(10), rect.y+s(56)))
                            cost_surf = font_xs.render(f"₺{cost}", True, (255,240,120))
                            screen.blit(cost_surf, (rect.right - cost_surf.get_width() - s(10), rect.y+s(8)))

                        try:
                            para_surf = font_xs.render(f"₺{cost}", True, (255,255,255))
                            box_w = para_surf.get_width() + s(8)
                            box_h = para_surf.get_height() + s(6)
                            box_x = rect.right - box_w - s(8)
                            box_y = rect.bottom - box_h - s(8)
                            pygame.draw.rect(screen, (12, 100, 200), (box_x, box_y, box_w, box_h), border_radius=6)
                            screen.blit(para_surf, (box_x + s(4), box_y + s(3)))
                        except Exception:
                            pass

                        feat['_rect'] = rect
                    else:
                        empty_rect = pygame.Rect(x, y, btn_w, btn_h)
                        pygame.draw.rect(screen, (30,30,36), empty_rect, border_radius=10)

                if page > 0:
                    pygame.draw.rect(screen, (60,60,80), left_rect, border_radius=8)
                    ltxt = font_big.render("◀", True, (255,255,255))
                    screen.blit(ltxt, ltxt.get_rect(center=left_rect.center))
                if page < total_pages - 1:
                    pygame.draw.rect(screen, (60,60,80), right_rect, border_radius=8)
                    rtxt = font_big.render("▶", True, (255,255,255))
                    screen.blit(rtxt, rtxt.get_rect(center=right_rect.center))

                pygame.draw.rect(screen, (200,80,80), back_rect, border_radius=10)
                btxt = font_mid.render("GERİ (Kapat)", True, (255,255,255))
                screen.blit(btxt, btxt.get_rect(center=back_rect.center))

                if show_confirm:
                    cm_w = min(s(780), width-s(120))
                    cm_h = s(220)
                    cm_rect = pygame.Rect((width-cm_w)//2, (height-cm_h)//2, cm_w, cm_h)
                    pygame.draw.rect(screen, (240,240,240), cm_rect, border_radius=12)
                    pygame.draw.rect(screen, (0,0,0), cm_rect, 3, border_radius=12)
                    qtxt = font_mid.render("Mağazayı kapatmak istiyor musun?", True, (0,0,0))
                    screen.blit(qtxt, (cm_rect.centerx - qtxt.get_width()//2, cm_rect.y + s(24)))
                    yes_rect = pygame.Rect(cm_rect.centerx - s(180), cm_rect.bottom - s(70), s(150), s(48))
                    no_rect = pygame.Rect(cm_rect.centerx + s(30), cm_rect.bottom - s(70), s(150), s(48))
                    pygame.draw.rect(screen, (60,140,60), yes_rect, border_radius=8)
                    pygame.draw.rect(screen, (180,50,50), no_rect, border_radius=8)
                    yes_t = font_mid.render("EVET", True, (255,255,255))
                    no_t = font_mid.render("HAYIR", True, (255,255,255))
                    screen.blit(yes_t, yes_t.get_rect(center=yes_rect.center))
                    screen.blit(no_t, no_t.get_rect(center=no_rect.center))

                pygame.display.flip()

                evs = pygame.event.get()
                for ev in evs:
                    if ev.type == pygame.QUIT:
                        running_shop = False
                        return
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_ESCAPE:
                            show_confirm = True
                        if ev.key == pygame.K_m:
                            show_confirm = True
                    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                        mx,my = ev.pos
                        if show_confirm:
                            if yes_rect.collidepoint((mx,my)):
                                running_shop = False
                                show_confirm = False
                                break
                            if no_rect.collidepoint((mx,my)):
                                show_confirm = False
                                continue
                        if left_rect.collidepoint((mx,my)) and page > 0:
                            page -= 1
                            continue
                        if right_rect.collidepoint((mx,my)) and page < total_pages - 1:
                            page += 1
                            continue
                        if back_rect.collidepoint((mx,my)):
                            running_shop = False
                            break
                        for i in range(per_page):
                            feat_idx = start_index + i
                            if feat_idx < total_features:
                                feat = FEATURES[feat_idx]
                                rect = feat.get('_rect')
                                if rect and rect.collidepoint((mx,my)):
                                    costk = feat["cost_key"]
                                    lvlk = feat["level_key"]
                                    cost = shop.get(costk, feat["base_cost"])
                                    lvl = shop.get(lvk := lvlk, 0)
                                    if lvl >= shop["max_per_feature"]:
                                        try: olumsuz_snd.play()
                                        except: pass
                                    elif money >= cost:
                                        money -= cost
                                        shop[lvlk] = lvl + 1
                                        shop[costk] = int(cost * 2)
                                        try:
                                            feat["apply_fn"](shop[lvlk])
                                        except Exception as e:
                                            log(f"feature apply error: {e}")
                                        try: olumlu_snd.play()
                                        except: pass
                                    else:
                                        try: olumsuz_snd.play()
                                        except: pass
                                    break
                                    save_current_profile()
                clock.tick(FPS)

            pause_end = pygame.time.get_ticks()
            pause_duration = pause_end - pause_start
            if pause_duration > 0:
                for c in customers:
                    c.start += pause_duration
                last_spawn += pause_duration

        # MAIN GAME LOOP
        running = True
        last_spawn = pygame.time.get_ticks()
        combo_count = 0
        combo_last_time = 0
        daily_counter = 0

        # Mode-specific variables
        mode_time_left = 60000  # for time attack (60s)
        if mode == "Süre Savaşı":
            mode_time_left = 60000

        while running:
            try:
                now = pygame.time.get_ticks()
                keys = pygame.key.get_pressed()
                def key_ok(k):
                    t = now
                    last = last_key_press_times.get(k, 0)
                    if t - last > DEBOUNCE_MS:
                        last_key_press_times[k] = t
                        return True
                    return False

                # T usage (time freeze) kept
                if keys[pygame.K_t] and key_ok('t'):
                    if shop.get("time_freeze_uses",0) > 0:
                        shop["time_freeze_uses"] -= 1
                        time_freeze_active_until = now + 5000

                # M opens shop
                if keys[pygame.K_m] and key_ok('m'):
                    shop_screen_pause()

                evs = pygame.event.get()
                for ev in evs:
                    if ev.type == pygame.QUIT:
                        if active_profile:
                            profiles[active_profile] = {
                                "happy": happy_total,
                                "money": money,
                                "shop": shop.copy()  # ✅ .copy() ekle (derin kopya)
                            }
                            save_profiles(profiles)
                            print(f"✅ QUIT - Kaydedildi: {active_profile}")  # ✅ Bilgi mesajı
                        append_score(active_profile or "Guest", happy_total)
                        pygame.quit()
                        return 0
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_ESCAPE:
                            if active_profile:
                                profiles[active_profile] = {"happy":happy_total,"money":money,"shop":shop}
                                save_profiles(profiles)
                            append_score(active_profile or "Guest", happy_total)
                            pygame.quit(); return 0
                        if ev.key == pygame.K_m and key_ok('m_event'):
                            shop_screen_pause()
                        if ev.key == pygame.K_t and key_ok('t_event'):
                            if shop.get("time_freeze_uses",0) > 0:
                                shop["time_freeze_uses"] -= 1
                                time_freeze_active_until = now + 5000

                # DRAW
                try:
                    screen.blit(pygame.transform.smoothscale(assets['background'], (width, height)), (0,0))
                except Exception:
                    screen.fill((30,30,30))
                screen.blit(counter, counter_rect)

                # ingredients area (with öğretici highlight)
                if öğretici_active and öğretici_step in (0,1,2):
                    map_step_to_name = {0:"wrap", 1:"meat", 2:"tomato"}
                    active_ing = map_step_to_name.get(öğretici_step, None)
                    draw_ingredients_with_highlight(active_ing)
                else:
                    for k, r in ingredient_rects.items():
                        screen.blit(ingredients[k], r)

                pygame.draw.rect(screen, (230,230,200), durum_area, border_radius=12)
                if not durum_done:
                    for i, it in enumerate(durum_items):
                        posc = (durum_area.centerx, durum_area.centery - i*s(14))
                        screen.blit(ingredients[it], ingredients[it].get_rect(center=posc))
                else:
                    if not dragging_doner:
                        screen.blit(ingredients['doner'], ingredients['doner'].get_rect(center=durum_area.center))

                pygame.draw.rect(screen, (50,140,60), dur_button, border_radius=8)
                dtxt = font_mid.render("DÜR", True, (255,255,255))
                screen.blit(dtxt, (dur_button.x + s(28), dur_button.y + s(8)))

                if dragging and drag_img:
                    mx,my = input_mgr.get_pos()
                    screen.blit(drag_img, drag_img.get_rect(center=(mx,my)))
                if dragging_doner and doner_rect:
                    mx,my = input_mgr.get_pos()
                    doner_rect.center = (mx,my)
                    screen.blit(ingredients['doner'], doner_rect)

                if öğretici_active:
                    öğretici_customer.draw()
                for c in customers:
                    c.draw()

                for tip in tip_messages[:]:
                    dt = now - tip.get("start",0)
                    if dt > 2200:
                        try: tip_messages.remove(tip)
                        except ValueError: pass
                    else:
                        y = tip.get("y", height-s(80)) - (dt * 0.06)
                        txt = font_mid.render(f"BAHŞİŞ ALDIN (+₺{tip.get('amount',0)})", True, (0,255,120))
                        rect = txt.get_rect(center=(width//2, int(y)))
                        screen.blit(txt, rect)

                money_s = font_mid.render(f"₺{money}", True, (255,220,50))
                screen.blit(money_s, (width - s(180), s(16)))
                happy_s = font_mid.render(f"Mutlu: {happy_total}", True, (255,255,255))
                screen.blit(happy_s, (width//2 - happy_s.get_width()//2, s(18)))

                if öğretici_active and öğretici_step < len(öğretici_steps_text):
                    hint_text = öğretici_steps_text[öğretici_step]
                    hint_surf = font_small.render(hint_text, True, (255,255,255))
                    screen.blit(hint_surf, (s(20), s(60)))

                hint = font_small.render("M: Mağaza  T: Zaman Dondurucu  ESC: Çıkış", True, (200,200,200))
                screen.blit(hint, (s(20), height - s(40)))

                # draw achievements popups
                draw_achievements()

                pygame.display.flip()
                clock.tick(FPS)

                # check achievements periodically
                check_achievements()

                # Mode-specific timer update
                if mode == "Süre Savaşı":
                    dt = clock.get_time()
                    mode_time_left -= dt
                    # draw timer on screen
                    timer_txt = font_mid.render(f"Süre: {max(0, mode_time_left//1000)}s", True, (255,200,60))
                    screen.blit(timer_txt, (width - s(360), s(60)))
                    # if time ended, finish game and show results
                    if mode_time_left <= 0:
                        # finalize: save profile and return to menu
                        if active_profile:
                            profiles[active_profile] = {"happy":happy_total,"money":money,"shop":shop}
                            save_profiles(profiles)
                        append_score(active_profile or "Guest", happy_total)
                        # show simple result popup
                        fade_out(400)
                        # display final screen
                        end_running = True
                        show_start = pygame.time.get_ticks()
                        while end_running:
                            for ev in pygame.event.get():
                                if ev.type == pygame.QUIT:
                                    pygame.quit(); return 0
                                if ev.type == pygame.KEYDOWN:
                                    end_running = False
                            screen.fill((12,12,20))
                            res = font_big.render(f"Time Attack Sonuç - Mutlu: {happy_total}", True, (255,255,255))
                            screen.blit(res, (width//2 - res.get_width()//2, height//2 - res.get_height()//2))
                            sub = font_small.render("Herhangi bir tuşa basın. (Menüye dönülecek)", True, (200,200,200))
                            screen.blit(sub, (width//2 - sub.get_width()//2, height//2 + s(40)))
                            pygame.display.flip()
                            clock.tick(FPS)
                        fade_in(400)
                        # reset and go back to menu
                        return 0

                # SPAWN (normal) - öğretici suppresses spawns until finished
                if öğretici_active:
                    spawn_allowed = False
                else:
                    if now < time_freeze_active_until:
                        spawn_allowed = False
                    else:
                        spawn_allowed = True

                effective_min = max(1200, int(spawn_min / (1.0 + 0.05 * shop.get('maxcust_level',0))))
                effective_max = max(3000, int(spawn_max / (1.0 + 0.05 * shop.get('maxcust_level',0))))
                spawn_try = False
                if spawn_allowed and now - last_spawn > random.randint(effective_min, effective_max):
                    spawn_try = True
                extra_spawn = shop.get('spawn_chance', 0.0)
                if not spawn_try and random.random() < extra_spawn:
                    spawn_try = True

                max_customers_allowed = base_max_customers + shop.get('maxcust_level',0)

                if spawn_try:
                    if len(customers) < max_customers_allowed:
                        slots = customer_slots.copy()
                        if len(slots) < max_customers_allowed:
                            for i in range(len(slots), max_customers_allowed):
                                slots.append(s(100) + i * (width - s(200)) // max_customers_allowed)
                        used_centers = [c.rect.centerx for c in customers]
                        free_slots = [s for s in slots if s not in used_centers]
                        if free_slots:
                            vip_chance = shop.get('vip_chance', 0.0) + (shop.get('vip_loyalty',0)*0.01)
                            is_vip = random.random() < vip_chance
                            slot = random.choice(free_slots)
                            level = shop.get("timer_level", 0)
                            if level <= 0:
                                timer_multiplier = 1.0
                            else:
                                timer_multiplier = 1.0 + 0.10 + 0.05 * max(0, level - 1)
                            pat_mult = shop.get('patience_multiplier',1.0)
                            cust_timer = int(base_customer_timer * timer_multiplier * pat_mult * shop.get('time_slow_multiplier',1.0))
                            # rich customers pay more
                            is_rich = random.random() < shop.get('rich_chance', 0.0)
                            customers.append(Customer(random.choice(cust_imgs), slot, cust_timer, vip=is_vip))
                            last_spawn = now
                            try: bell.play()
                            except: pass

                # pointer events (mouse + touch)
                for p_kind, p_pos in input_mgr.iter_pointer(evs):
                    if p_kind == 'down':
                        px, py = p_pos
                        # allow dragging from ingredient rects
                        if not durum_done:
                            for name, rect in ingredient_rects.items():
                                if rect.collidepoint((px,py)):
                                    dragging = True
                                    drag_item = name
                                    drag_img = ingredients[name]
                                    break
                        # DUR pressed
                        if dur_button.collidepoint((px,py)) and wrap_placed and not durum_done:
                            if öğretici_active and öğretici_step == 3:
                                play_random_good()
                                öğretici_step = 4
                                try: öğretici_voices[4].play()
                                except: pass
                            durum_done = True
                            dragging = False
                            drag_item = None
                            drag_img = None
                            doner_rect = ingredients['doner'].get_rect(center=durum_area.center)
                        # start dragging doner to give to customer
                        if durum_done and doner_rect and doner_rect.collidepoint((px,py)):
                            dragging_doner = True

                    elif p_kind == 'up':
                        ux, uy = p_pos
                        if dragging:
                            dragging = False
                            # drop into durum area?
                            if durum_area.collidepoint((ux,uy)):
                                if drag_item == "wrap" and not wrap_placed:
                                    durum_items = ["wrap"]
                                    wrap_placed = True
                                    if öğretici_active:
                                        öğretici_place_check("wrap")
                                elif wrap_placed and drag_item != "wrap" and drag_item not in durum_items:
                                    durum_items.append(drag_item)
                                    if öğretici_active:
                                        if drag_item in ("meat","tomato"):
                                            öğretici_place_check(drag_item)
                            drag_item = None
                            drag_img = None

                        if dragging_doner:
                            dragging_doner = False
                            delivered = False
                            if öğretici_active:
                                if öğretici_customer.rect.collidepoint((ux,uy)):
                                    expected = set(öğretici_customer.order)
                                    given = set(durum_items) - {"wrap"}
                                    if expected == given:
                                        # success
                                        play_success()
                                        happy_total += 1
                                        total_sold += 1
                                        money += 20
                                        try: teslim_voice.play()
                                        except: pass
                                        delivered = True
                                        # öğretici complete if last step
                                        if öğretici_step >= 3:
                                            öğretici_active = False
                                            öğretici_step = 0
                                            try:
                                                son = safe_sound(resource_path(f"{ASSETS_DIR}/son.mp3"))
                                                pygame.time.delay(2500)
                                                son.play()
                                            except:
                                                pass
                                    else:
                                        play_fail()
                                        money -= 5
                                        delivered = True
                                # reset durum
                                durum_items = []
                                wrap_placed = False
                                durum_done = False
                                doner_rect = None
                            else:
                                # normal delivery: check customers list
                                for c in customers:
                                    if c.rect.collidepoint((ux,uy)):
                                        # compare order
                                        expected = set(c.order)
                                        given = set(durum_items) - {"wrap"}
                                        if expected == given:
                                            play_success()
                                            happy_total += 1
                                            total_sold += 1
                                            gain = 20
                                            if c.is_vip:
                                                gain = int(gain * shop.get('vip_multiplier', 1.0))
                                            money += gain
                                            # tips
                                            if random.random() < shop.get('tip_chance', 0.05):
                                                amt = random.randint(shop.get('tip_amount_min',1), shop.get('tip_amount_max',5))
                                                tip_messages.append({"start": pygame.time.get_ticks(), "amount": amt, "y": height - s(140)})
                                                money += amt
                                            # remove customer
                                            try: customers.remove(c)
                                            except ValueError: pass
                                            delivered = True
                                        else:
                                            play_fail()
                                            money -= 7
                                            # anger -> customer leaves faster
                                            try: customers.remove(c)
                                            except ValueError: pass
                                            delivered = True
                                        break
                                durum_items = []
                                wrap_placed = False
                                durum_done = False
                                doner_rect = None
                            # achievement check
                            check_achievements()

                # handle customer timeouts
                for c in customers[:]:
                    elapsed = pygame.time.get_ticks() - c.start
                    if elapsed > c.timer:
                        # customer leaves unhappy
                        try: customers.remove(c)
                        except ValueError: pass
                        money -= 3
                        # possible return chance
                        if random.random() < shop.get('return_chance', 0.0):
                            # schedule return later (simple)
                            customers.append(Customer(random.choice(cust_imgs), random.choice(customer_slots), base_customer_timer, vip=False))

                # small performance guard: cap customer list
                if len(customers) > 20:
                    customers = customers[:20]

            # end main loop try
            except Exception as e:
                crash_log(e)
                try:
                    pygame.quit()
                except:
                    pass
                return 1

        # end run_game try
    except Exception as e:
        crash_log(e)
        try:
            pygame.quit()
        except Exception:
            pass
        return 1

if __name__ == "__main__":
    sys.exit(run_game())



# ==== FINAL v3 PATCH: Documents save path, autoplay intro, remove admin prompts ====
import os, json, traceback
try:
    import pygame
except Exception:
    pygame = None

print("[FINAL v3 PATCH] Applying Documents save path and intro autoplay...")

def get_documents_dir(app_folder="ATAGULDONER"):
    try:
        user = os.environ.get("USERPROFILE") or os.path.expanduser("~")
        docs = os.path.join(user, "Documents")
        if not os.path.exists(docs):
            docs = os.path.join(os.path.expanduser("~"), "Documents")
        base = os.path.join(docs, app_folder)
        os.makedirs(base, exist_ok=True)
        return base
    except Exception:
        base = os.path.join(os.path.abspath("."), app_folder)
        os.makedirs(base, exist_ok=True)
        return base

DOCS_DIR = get_documents_dir("ATAGULDONER")
DOCS_USERDATA = os.path.join(DOCS_DIR, "userdata.json")
DOCS_SETTINGS = os.path.join(DOCS_DIR, "settings.json")

def load_userdata_docs():
    try:
        if os.path.exists(DOCS_USERDATA):
            with open(DOCS_USERDATA, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_userdata_docs(data):
    try:
        with open(DOCS_USERDATA, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        try:
            with open("userdata_fallback.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

globals().setdefault("DOCS_DIR", DOCS_DIR)
globals().setdefault("DOCS_USERDATA", DOCS_USERDATA)
globals().setdefault("DOCS_SETTINGS", DOCS_SETTINGS)
globals().setdefault("load_userdata_docs", load_userdata_docs)
globals().setdefault("save_userdata_docs", save_userdata_docs)

# If profiles not set, load from documents
if "profiles" not in globals() or not globals().get("profiles"):
    try:
        globals()["profiles"] = load_userdata_docs() or {}
    except Exception:
        globals()["profiles"] = {}

# Avoid writing to Program Files by setting flags
globals().setdefault("ALLOW_PROGRAM_FILES_WRITE", False)
globals().setdefault("FORCE_SAVE_TO_DOCUMENTS", True)

# Autoplay intro if function exists
def autoplay_intro_safe():
    try:
        if "play_intro_video" in globals() and callable(globals()["play_intro_video"]):
            try:
                globals()["play_intro_video"]()
            except Exception:
                pass
    except Exception:
        pass

if "pre_main_wrapper" in globals() and callable(globals()["pre_main_wrapper"]):
    try:
        orig = globals()["pre_main_wrapper"]
        def new_pre_main_wrapper():
            try:
                autoplay_intro_safe()
            except Exception:
                pass
            try:
                return orig()
            except Exception:
                return None
        globals()["pre_main_wrapper"] = new_pre_main_wrapper
    except Exception:
        globals()["pre_main_wrapper"] = autoplay_intro_safe
else:
    globals()["pre_main_wrapper"] = autoplay_intro_safe

print("[FINAL v3 PATCH] Documents path:", DOCS_DIR)


# PADDING START
# pad_line_0
# pad_line_1
# pad_line_2
# pad_line_3
# pad_line_4
# pad_line_5
# pad_line_6
# pad_line_7
# pad_line_8
# pad_line_9
# pad_line_10
# pad_line_11
# pad_line_12
# pad_line_13
# pad_line_14
# pad_line_15
# pad_line_16
# pad_line_17
# pad_line_18
# pad_line_19
# pad_line_20
# pad_line_21
# pad_line_22
# pad_line_23
# pad_line_24
# pad_line_25
# pad_line_26
# pad_line_27
# pad_line_28
# pad_line_29
# pad_line_30
# pad_line_31
# pad_line_32
# pad_line_33
# pad_line_34
# pad_line_35
# pad_line_36
# pad_line_37
# pad_line_38
# pad_line_39
# pad_line_40
# pad_line_41
# pad_line_42
# pad_line_43
# pad_line_44
# pad_line_45
# pad_line_46
# pad_line_47
# pad_line_48
# pad_line_49
# pad_line_50
# pad_line_51
# pad_line_52
# pad_line_53
# pad_line_54
# pad_line_55
# pad_line_56
# pad_line_57
# pad_line_58
# pad_line_59
# pad_line_60
# pad_line_61
# pad_line_62
# pad_line_63
# pad_line_64
# pad_line_65
# pad_line_66
# pad_line_67
# pad_line_68
# pad_line_69
# pad_line_70
# pad_line_71
# pad_line_72
# pad_line_73
# pad_line_74
# pad_line_75
# pad_line_76
# pad_line_77
# pad_line_78
# pad_line_79
# pad_line_80
# pad_line_81
# pad_line_82
# pad_line_83
# pad_line_84
# pad_line_85
# pad_line_86
# pad_line_87
# pad_line_88
# pad_line_89
# pad_line_90
# pad_line_91
# pad_line_92
# pad_line_93
# pad_line_94
# pad_line_95
# pad_line_96
# pad_line_97
# pad_line_98
# pad_line_99
# pad_line_100
# pad_line_101
# pad_line_102
# pad_line_103
# pad_line_104
# pad_line_105
# pad_line_106
# pad_line_107
# pad_line_108
# pad_line_109
# pad_line_110
# pad_line_111
# pad_line_112
# pad_line_113
# pad_line_114
# pad_line_115
# pad_line_116
# pad_line_117
# pad_line_118
# pad_line_119
# pad_line_120
# pad_line_121
# pad_line_122
# pad_line_123
# pad_line_124
# pad_line_125
# pad_line_126
# pad_line_127
# pad_line_128
# pad_line_129
# pad_line_130
# pad_line_131
# pad_line_132
# pad_line_133
# pad_line_134
# pad_line_135
# pad_line_136
# pad_line_137
# pad_line_138
# pad_line_139
# pad_line_140
# pad_line_141
# pad_line_142
# pad_line_143
# pad_line_144
# pad_line_145
# pad_line_146
# pad_line_147
# pad_line_148
# pad_line_149
# pad_line_150
# pad_line_151
# pad_line_152
# pad_line_153
# pad_line_154
# pad_line_155
# pad_line_156
# pad_line_157
# pad_line_158
# pad_line_159
# pad_line_160
# pad_line_161
# pad_line_162
# pad_line_163
# pad_line_164
# pad_line_165
# pad_line_166
# pad_line_167
# pad_line_168
# pad_line_169
# pad_line_170
# pad_line_171
# pad_line_172
# pad_line_173
# pad_line_174
# pad_line_175
# pad_line_176
# pad_line_177
# pad_line_178
# pad_line_179
# pad_line_180
# pad_line_181
# pad_line_182
# pad_line_183
# pad_line_184
# pad_line_185
# pad_line_186
# pad_line_187
# pad_line_188
# pad_line_189
# pad_line_190
# pad_line_191
# pad_line_192
# pad_line_193
# pad_line_194
# pad_line_195
# pad_line_196
# PADDING END



# ===== FINAL v4 INTEGRATION =====
# Appended: enforce true 60s gameplay timer, profile-create-on-classic-entry,
# ESC save & confirm ties, Documents saving, UI scaling enforcement, intro autoplay (game.mp4).
import os, time, json, traceback
try:
    import pygame
except Exception:
    pygame = None

print("[FINAL v4] Integration applying...")

# Documents path helpers (Unreal-like Documents save)
def get_docs_dir(app_name="ATAGULDONER"):
    try:
        user = os.environ.get("USERPROFILE") or os.path.expanduser("~")
        docs = os.path.join(user, "Documents")
        if not os.path.exists(docs):
            docs = os.path.join(os.path.expanduser("~"), "Documents")
        base = os.path.join(docs, app_name)
        os.makedirs(base, exist_ok=True)
        return base
    except Exception:
        base = os.path.join(os.path.abspath("."), app_name)
        os.makedirs(base, exist_ok=True)
        return base

DOCS_DIR = get_docs_dir("ATAGULDONER")
DOCS_USERDATA = os.path.join(DOCS_DIR, "userdata.json")

def load_docs_userdata():
    try:
        if os.path.exists(DOCS_USERDATA):
            with open(DOCS_USERDATA, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_docs_userdata(data):
    try:
        with open(DOCS_USERDATA, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        try:
            with open("userdata_fallback.json","w",encoding="utf-8") as f:
                json.dump(data,f,ensure_ascii=False,indent=2)
        except Exception:
            pass

# Ensure global profiles point to Documents data
globals().setdefault("profiles", load_docs_userdata())
if not globals().get("profiles"):
    globals()["profiles"] = {}

# UI scaling helper (enforced)
BASE_W = globals().get("BASE_W", 1920)
BASE_H = globals().get("BASE_H", 1080)
def s(px):
    try:
        if pygame and pygame.display.get_surface():
            w,h = pygame.display.get_surface().get_size()
            scale = min(max(0.5, w/BASE_W), max(0.5, h/BASE_H))
            return max(1, int(px * scale))
    except Exception:
        pass
    return px
globals()["s"] = s

# True 60-second timer helper for gameplay loops
def run_60s_mode(game_loop_fn, on_end_fn=None):
    """
    game_loop_fn: a callable that will be called each frame with remaining_time (float seconds)
    on_end_fn: callable(score) called when time ends
    This helper manages a 60.0 second countdown ensuring real-time behavior.
    """
    start = time.time()
    duration = 60.0
    score = 0
    running = True
    try:
        # provide a simple frame loop; rely on game_loop_fn to draw and process events
        while running:
            elapsed = time.time() - start
            remaining = max(0.0, duration - elapsed)
            # call provided frame handler
            try:
                # If game_loop_fn returns a dict with control signals, respect them
                res = game_loop_fn(remaining)
                if isinstance(res, dict):
                    if res.get("exit"):
                        running = False
                        break
                    if res.get("score") is not None:
                        score = res.get("score")
                # early exit if time reached
            except Exception:
                pass
            if remaining <= 0.0:
                running = False
                break
            # small sleep to avoid busy loop (frame cap handled by game)
            time.sleep(0.01)
    except Exception:
        traceback.print_exc()
    # call on_end_fn
    try:
        if callable(on_end_fn):
            on_end_fn(score)
    except Exception:
        pass
    return score

globals().setdefault("run_60s_mode", run_60s_mode)

# Hook: when entering Classic mode, ensure profile exists or redirect to profile creation UI.
def ensure_profile_for_classic(redirect_fn=None, create_ui_fn=None):
    """
    redirect_fn(): called to navigate to profile menu (if provided)
    create_ui_fn(): if provided, will be used to prompt for a name and return profile name
    """
    try:
        profiles = globals().get("profiles", {})
        active = globals().get("active_profile", None)
        if active and active in profiles:
            return active
        # if no profiles exist, create default or call create_ui_fn
        if create_ui_fn and callable(create_ui_fn):
            try:
                name = create_ui_fn()
                if not name:
                    name = "Oyuncu1"
            except Exception:
                name = "Oyuncu1"
        else:
            # create automatic profile
            name = "Oyuncu1"
        # add to profiles and save
        profiles.setdefault(name, {"money":0,"rank":"","happy":0,"missions":[]})
        globals()["profiles"] = profiles
        globals()["active_profile"] = name
        try:
            save_docs_userdata(profiles)
        except Exception:
            pass
        # if redirect_fn provided, call to navigate UI
        if redirect_fn and callable(redirect_fn):
            try:
                redirect_fn("profile_menu")
            except Exception:
                pass
        return name
    except Exception:
        return None

globals().setdefault("ensure_profile_for_classic", ensure_profile_for_classic)

# ESC: integrate with existing pause_and_confirm or provide fallback that saves to Documents
def global_pause_and_save(screen=None, font=None):
    try:
        # prefer existing pause_and_confirm if present
        if "pause_and_confirm" in globals() and callable(globals()["pause_and_confirm"]):
            res = globals()["pause_and_confirm"](screen=screen, font=font)
            # if pause_and_confirm saved, ensure docs save
            try:
                save_docs_userdata(globals().get("profiles", {}))
            except Exception:
                pass
            return res
        # fallback minimal UI: save and return False (do not exit)
        try:
            save_docs_userdata(globals().get("profiles", {}))
        except Exception:
            pass
        return False
    except Exception:
        return False

globals()["global_pause_and_save"] = global_pause_and_save

# Intro autoplay enforcement: ensure game.mp4 is used at startup (non-blocking wrapper)
def autoplay_intro_nonblocking(vid_name="game.mp4"):
    try:
        if "play_intro_video" in globals() and callable(globals()["play_intro_video"]):
            try:
                globals()["play_intro_video"](vid_name)
            except Exception:
                pass
    except Exception:
        pass

globals().setdefault("autoplay_intro_nonblocking", autoplay_intro_nonblocking)

print("[FINAL v4] Integration complete. Documents user data path:", DOCS_USERDATA)
# ===== END FINAL v4 =====





# ---------------------- INTEGRATION & STABILITY PATCH (START) ----------------------
# This patch enforces:
# - Single "Klasik" mode (removes Zen / 60s options by overriding menu functions)
# - Profile system saved in Documents/ATAGULDONER with encryption fallback
# - Aggressive autosave and wrappers for key functions
# - Shop pause/resume enforcement
# - Surface device detection and blocking message
# - Final save on exit
import os, sys, json, threading, time, atexit, platform, subprocess, pickle, traceback

SAVE_DIR = os.path.join(os.path.expanduser("~"), "Documents", "ATAGULDONER")
os.makedirs(SAVE_DIR, exist_ok=True)
SAVE_FILE = "profiles.dat"

# Simple encrypt/decrypt using XOR + base64 as a fallback if no better method exists
try:
    import base64, hashlib
    _SECRET_KEY = hashlib.sha256(b"AtagulDonerSecretKey_v1").digest()
    def encrypt_bytes(b: bytes) -> bytes:
        # XOR with secret key repeated, then base64 encode
        out = bytearray(len(b))
        for i in range(len(b)):
            out[i] = b[i] ^ _SECRET_KEY[i % len(_SECRET_KEY)]
        return base64.b64encode(bytes(out))

    def decrypt_bytes(b: bytes) -> bytes:
        try:
            raw = base64.b64decode(b)
        except Exception:
            return None
        out = bytearray(len(raw))
        for i in range(len(raw)):
            out[i] = raw[i] ^ _SECRET_KEY[i % len(_SECRET_KEY)]
        return bytes(out)
except Exception:
    def encrypt_bytes(b): return b
    def decrypt_bytes(b): return b

def _profiles_path():
    return os.path.join(SAVE_DIR, SAVE_FILE)

def load_profiles() -> dict:
    pth = _profiles_path()
    if os.path.exists(pth):
        try:
            with open(pth, "rb") as f:
                blob = f.read()
            try:
                dec = decrypt_bytes(blob)
                if dec is not None:
                    return json.loads(dec.decode("utf-8"))
            except Exception:
                pass
            try:
                return pickle.loads(blob)
            except Exception:
                pass
        except Exception as e:
            print("load_profiles error:", e)
    return {}

def save_profiles(profiles: dict):
    pth = _profiles_path()
    try:
        data = json.dumps(profiles, ensure_ascii=False).encode("utf-8")
        try:
            enc = encrypt_bytes(data)
            with open(pth, "wb") as f:
                f.write(enc)
            return
        except Exception:
            pass
        try:
            with open(pth, "wb") as f:
                pickle.dump(profiles, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print("save_profiles pickle error:", e)
    except Exception as e:
        print("save_profiles outer error:", e)

# Load existing profiles global variable (module-level)
try:
    profiles = load_profiles()
except Exception:
    profiles = {}

active_profile = None

# Helper: create profile if none exists
def ensure_profile(name="Player1"):
    global active_profile, profiles
    if not profiles:
        profiles[name] = {
            "money": 0,
            "score": 0,
            "items": {},
            "level": 1,
            "last_played": time.time()
        }
        active_profile = name
        save_profiles(profiles)
    else:
        if active_profile is None:
            # pick first profile
            active_profile = next(iter(profiles.keys()))
    return active_profile

# Aggressive save helper
def safe_save():
    global profiles
    try:
        if isinstance(profiles, dict):
            # update last_played timestamp for active profile
            try:
                if active_profile and active_profile in profiles:
                    profiles[active_profile]["last_played"] = time.time()
            except Exception:
                pass
            save_profiles(profiles)
    except Exception as e:
        print("safe_save error:", e)
        try:
            # fallback backup
            backup = os.path.join(SAVE_DIR, "profiles_backup.json")
            with open(backup, "w", encoding="utf-8") as f:
                json.dump(profiles, f, ensure_ascii=False)
        except Exception:
            pass

# Autosave thread that writes when snapshots differ
def _autosave_loop(interval=2.0):
    global profiles
    last = None
    while True:
        try:
            cur = json.dumps(profiles, sort_keys=True, ensure_ascii=False)
            if cur != last:
                save_profiles(profiles)
                last = cur
        except Exception:
            pass
        time.sleep(interval)

try:
    t_autosave = threading.Thread(target=_autosave_loop, args=(2.0,), daemon=True)
    t_autosave.start()
except Exception:
    pass

atexit.register(safe_save)

# Surface device detection - block with message
def _is_surface_device():
    try:
        s = ' '.join([str(platform.uname().system), str(platform.uname().node), str(platform.uname().release), str(platform.uname().version), str(platform.uname().machine)]).lower()
        if 'surface' in s:
            return True
        if sys.platform.startswith('win'):
            try:
                out = subprocess.check_output(['wmic', 'computersystem', 'get', 'model'], stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, timeout=1, universal_newlines=True)
                if 'surface' in out.lower():
                    return True
            except Exception:
                pass
    except Exception:
        pass
    return False

def _show_surface_block_pygame():
    try:
        import pygame as _pg
        _pg.init()
        sw, sh = 800, 300
        win = _pg.display.set_mode((sw, sh))
        _pg.display.set_caption("UYARI - Cihaz Desteklenmiyor")
        font = _pg.font.SysFont(None, 28)
        lines = ["Bu cihaz için çalışmalarımız sürüyor.", "Lütfen farklı bir cihazda oyunu çalıştırın."]
        win.fill((30,30,30))
        for i, line in enumerate(lines):
            surf = font.render(line, True, (255,255,255))
            win.blit(surf, (20, 80 + i*36))
        _pg.display.flip()
        t0 = time.time()
        while time.time() - t0 < 3.0:
            for ev in _pg.event.get():
                if ev.type == _pg.QUIT:
                    break
            time.sleep(0.05)
        try:
            _pg.quit()
        except Exception:
            pass
    except Exception:
        print("Surface detected - please use another device.")

# Immediately block if Surface detected (Windows)
try:
    if sys.platform.startswith('win') and _is_surface_device():
        _show_surface_block_pygame()
        print("Surface device blocked by policy. Exiting.")
        sys.exit(0)
except Exception:
    pass

# Override menu/mode selection functions if present in the base file.
# We'll attempt to replace common function names to force single mode behavior.
def _force_single_mode_overrides(globals_dict):
    # Replace mode list and menu drawers if present
    try:
        # If there's a variable named MODES or mode_options, set to ["Klasik"]
        if 'MODES' in globals_dict:
            globals_dict['MODES'] = ["Klasik"]
        if 'mode_options' in globals_dict:
            globals_dict['mode_options'] = ["Klasik"]
        # Override any function named show_mode_menu / mode_select_screen / main_menu to force single choice
        for fname in ('mode_select_screen', 'show_mode_menu', 'main_menu', 'draw_mode_menu'):
            if fname in globals_dict and callable(globals_dict[fname]):
                def _single_menu_wrapper(*a, __orig=globals_dict[fname], **k):
                    # attempt to call original but return "Klasik" or a consistent choice
                    try:
                        res = __orig(*a, **k)
                    except Exception:
                        res = None
                    # return standardized mode selection
                    return "Klasik"
                globals_dict[fname] = _single_menu_wrapper
    except Exception:
        pass

# Wrappers for shop pause/resume - try to find functions and wrap them
def _wrap_shop_functions(globals_dict):
    for shop_name in ('shop_screen', 'shop', 'open_shop', 'shop_screen_pause', 'show_shop'):
        if shop_name in globals_dict and callable(globals_dict[shop_name]):
            orig = globals_dict[shop_name]
            def _shop_wrapper(*a, __o=orig, **k):
                # attempt to pause game state if there's a pause_game function
                try:
                    if 'pause_game' in globals_dict and callable(globals_dict['pause_game']):
                        globals_dict['pause_game']()
                except Exception:
                    pass
                try:
                    res = __o(*a, **k)
                except Exception as e:
                    print("shop wrapper error:", e)
                    res = None
                try:
                    safe_save()
                except Exception:
                    pass
                # resume if resume available
                try:
                    if 'resume_game' in globals_dict and callable(globals_dict['resume_game']):
                        globals_dict['resume_game']()
                except Exception:
                    pass
                return res
            globals_dict[shop_name] = _shop_wrapper

# Attempt to apply overrides into current module globals (this file is executed after base content)
try:
    _force_single_mode_overrides(globals())
    _wrap_shop_functions(globals())
except Exception:
    pass

# Monkeypatch common state-changing functions by name to call safe_save after execution
_common_state_funcs = [
    'add_money', 'give_money', 'set_money', 'purchase_item', 'buy_item', 'shop_buy', 'complete_level',
    'level_complete', 'create_profile', 'new_profile', 'grant_item', 'add_item_to_profile', 'use_item'
]
for fname in _common_state_funcs:
    try:
        if fname in globals() and callable(globals()[fname]):
            orig = globals()[fname]
            def _make_wrapper(f):
                def _wrapped(*a, __f=f, **k):
                    res = None
                    try:
                        res = __f(*a, **k)
                    except Exception as e:
                        try:
                            safe_save()
                        except Exception:
                            pass
                        raise
                    try:
                        safe_save()
                    except Exception:
                        pass
                    return res
                return _wrapped
            globals()[fname] = _make_wrapper(orig)
    except Exception:
        pass

# Final status print
print("Integration patch applied: single-mode enforced, autosave active, profiles path:", _profiles_path())

# ---------------------- INTEGRATION & STABILITY PATCH (END) ----------------------
