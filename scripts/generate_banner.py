import os
import math
from PIL import Image
import numpy as np

# ==============================================================================
# LOCKED PORTRAIT GENERATION (DO NOT ALTER PORTRAIT CROPPING / DENSITY)
# ==============================================================================

def crop_head_and_shoulders(img):
    w, h = img.size
    x1 = int(w * 0.18)
    y1 = int(h * 0.05)
    x2 = int(w * 0.82)
    y2 = int(h * 0.67)
    cropped = img.crop((x1, y1, x2, y2))
    return cropped

def process_image_to_dots(img_cropped, cols=68, rows=68):
    resized = img_cropped.resize((cols, rows), Image.Resampling.LANCZOS)
    arr = np.array(resized.convert('RGB'))
    bg_ref = np.array([196, 190, 190])
    
    dots_data = []
    for r in range(rows):
        for c in range(cols):
            rgb = arr[r, c]
            dist = float(np.linalg.norm(rgb.astype(float) - bg_ref))
            lum = float(0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
            is_bg = (dist < 40) and (lum > 145)
            dots_data.append((c, r, lum, is_bg, dist))
            
    return cols, rows, dots_data

# ==============================================================================
# MORPH STATES GENERATORS (STRICT LOCAL COORDINATES)
# ==============================================================================

def create_python_state(ui_cyan, accent_violet, panel_bg, text_primary):
    return f'''<g id="python-state-inner">
        <rect x="-100" y="-85" width="200" height="170" rx="14" fill="{panel_bg}" stroke="{ui_cyan}" stroke-width="2" opacity="0.96" />
        <g transform="translate(0, -12) scale(2.2) translate(-24, -24)">
          <path d="M 23.85 2 C 12.78 2 13.4 6.8 13.4 6.8 L 13.43 11.77 L 24.3 11.77 L 24.3 13.33 L 8.9 13.33 C 8.9 13.33 2 12.56 2 23.77 C 2 35 7.9 34.5 7.9 34.5 L 11.4 34.5 L 11.4 29.5 C 11.4 29.5 11.1 23.4 17.3 23.4 L 28.1 23.4 C 28.1 23.4 34.1 23.4 34.1 17.5 L 34.1 7.7 C 34.1 7.7 34.9 2 23.85 2 Z M 18.2 5.5 C 19.3 5.5 20.2 6.4 20.2 7.5 C 20.2 8.6 19.3 9.5 18.2 9.5 C 17.1 9.5 16.2 8.6 16.2 7.5 C 16.2 6.4 17.1 5.5 18.2 5.5 Z" fill="{ui_cyan}" />
          <path d="M 24.15 46 C 35.2 46 34.6 41.2 34.6 41.2 L 34.57 36.23 L 23.7 36.23 L 23.7 34.67 L 39.1 34.67 C 39.1 34.67 46 35.44 46 24.23 C 46 13 40.1 13.5 40.1 13.5 L 36.6 13.5 L 36.6 18.5 C 36.6 18.5 36.9 24.6 30.7 24.6 L 19.9 24.6 C 19.9 24.6 13.9 24.6 13.9 30.5 L 13.9 40.3 C 13.9 40.3 13.1 46 24.15 46 Z M 29.8 42.5 C 28.7 42.5 27.8 41.6 27.8 40.5 C 27.8 39.4 28.7 38.5 29.8 38.5 C 30.9 38.5 31.8 39.4 31.8 40.5 C 31.8 41.6 30.9 42.5 29.8 42.5 Z" fill="{accent_violet}" />
        </g>
        <text x="0" y="58" class="font-mono txt-primary" font-size="13" font-weight="700" text-anchor="middle" letter-spacing="2">PYTHON ENGINE</text>
      </g>'''

def create_ai_state(ui_cyan, accent_violet, success_green, header_bg, panel_bg, text_primary):
    return f'''<g id="ai-state-inner">
        <rect x="-100" y="-85" width="200" height="170" rx="14" fill="{panel_bg}" stroke="{accent_violet}" stroke-width="2" opacity="0.96" />
        <g transform="translate(0, -12)">
          <line x1="-55" y1="-32" x2="0" y2="-52" stroke="{ui_cyan}" stroke-width="2" opacity="0.75" />
          <line x1="-55" y1="-32" x2="0" y2="0" stroke="{ui_cyan}" stroke-width="2" opacity="0.75" />
          <line x1="-55" y1="32" x2="0" y2="0" stroke="{ui_cyan}" stroke-width="2" opacity="0.75" />
          <line x1="-55" y1="32" x2="0" y2="52" stroke="{ui_cyan}" stroke-width="2" opacity="0.75" />
          
          <line x1="0" y1="-52" x2="55" y2="-25" stroke="{accent_violet}" stroke-width="2" opacity="0.85" />
          <line x1="0" y1="0" x2="55" y2="-25" stroke="{accent_violet}" stroke-width="2" opacity="0.85" />
          <line x1="0" y1="0" x2="55" y2="25" stroke="{accent_violet}" stroke-width="2" opacity="0.85" />
          <line x1="0" y1="52" x2="55" y2="25" stroke="{accent_violet}" stroke-width="2" opacity="0.85" />
          
          <circle cx="-55" cy="-32" r="9" fill="{header_bg}" stroke="{ui_cyan}" stroke-width="2.5" />
          <circle cx="-55" cy="32" r="9" fill="{header_bg}" stroke="{ui_cyan}" stroke-width="2.5" />
          
          <circle cx="0" cy="-52" r="10" fill="{header_bg}" stroke="{accent_violet}" stroke-width="2.5" />
          <circle cx="0" cy="0" r="12" fill="{header_bg}" stroke="{ui_cyan}" stroke-width="2.5" />
          <circle cx="0" cy="52" r="10" fill="{header_bg}" stroke="{accent_violet}" stroke-width="2.5" />
          
          <circle cx="55" cy="-25" r="9" fill="{header_bg}" stroke="{success_green}" stroke-width="2.5" />
          <circle cx="55" cy="25" r="9" fill="{header_bg}" stroke="{success_green}" stroke-width="2.5" />
          
          <circle cx="0" cy="0" r="4" fill="{ui_cyan}" />
          <circle cx="55" cy="-25" r="3.5" fill="{success_green}" />
          <circle cx="55" cy="25" r="3.5" fill="{success_green}" />
        </g>
        <text x="0" y="58" class="font-mono txt-primary" font-size="13" font-weight="700" text-anchor="middle" letter-spacing="2">MACHINE LEARNING</text>
      </g>'''

def create_code_state(ui_cyan, accent_violet, success_green, panel_bg, text_primary):
    return f'''<g id="code-state-inner">
        <rect x="-100" y="-85" width="200" height="170" rx="14" fill="{panel_bg}" stroke="{success_green}" stroke-width="2" opacity="0.96" />
        <g transform="translate(0, -12)">
          <path d="M -42 -20 L -62 0 L -42 20" fill="none" stroke="{ui_cyan}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
          <path d="M 42 -20 L 75 0 L 50 25" fill="none" stroke="{ui_cyan}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
          <line x1="14" y1="-30" x2="-14" y2="30" stroke="{accent_violet}" stroke-width="6" stroke-linecap="round" />
        </g>
        <text x="0" y="58" class="font-mono txt-primary" font-size="13" font-weight="700" text-anchor="middle" letter-spacing="2">SOFTWARE DEV</text>
      </g>'''

# ==============================================================================
# MAIN BANNER GENERATOR
# ==============================================================================

def generate_svg(theme="dark", mode="animated", forced_state=None):
    is_dark = (theme == "dark")
    
    # Theme Tokens
    bg_main = "#0A101F" if is_dark else "#F8FAFC"
    panel_bg = "#0F172A" if is_dark else "#FFFFFF"
    panel_border = "#1E293B" if is_dark else "#CBD5E1"
    header_bg = "#1E293B" if is_dark else "#F1F5F9"
    header_border = "#334155" if is_dark else "#E2E8F0"
    
    ui_cyan = "#22D3EE" if is_dark else "#0891B2"
    accent_violet = "#A78BFA" if is_dark else "#7C3AED"
    accent_bright = "#C4B5FD" if is_dark else "#6D28D9"
    success_green = "#10B981" if is_dark else "#059669"
    
    text_primary = "#F8FAFC" if is_dark else "#0F172A"
    text_muted = "#94A3B8" if is_dark else "#64748B"
    text_dim = "#475569" if is_dark else "#94A3B8"
    leader_color = "#334155" if is_dark else "#E2E8F0"
    
    # Load source photo
    img_path = "assets/pranav-profile.png"
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Source portrait not found at {img_path}")
        
    img = Image.open(img_path)
    cropped = crop_head_and_shoulders(img)
    cols, rows, dots_data = process_image_to_dots(cropped, cols=68, rows=68)
    
    # Viewport Bounds (LOCKED)
    vp_x, vp_y, vp_w, vp_h = 58, 118, 404, 385
    center_x = vp_x + vp_w / 2.0  # 260.0
    center_y = vp_y + vp_h / 2.0  # 310.5
    symbol_center_y = center_y - 20.0  # 290.5
    
    dx = vp_w / cols
    dy = vp_h / rows
    
    portrait_circles = []
    for c, r, lum, is_bg, dist in dots_data:
        cx = vp_x + (c + 0.5) * dx
        cy = vp_y + (r + 0.5) * dy
        
        if is_bg:
            continue
            
        norm_darkness = (255.0 - lum) / 255.0
        
        if is_dark:
            if norm_darkness > 0.55:
                radius = 1.2 + (norm_darkness ** 1.3) * 1.8
                fill = accent_violet
                opacity = 0.95
            elif norm_darkness > 0.35:
                radius = 0.9 + norm_darkness * 1.3
                fill = accent_bright
                opacity = 0.85
            else:
                radius = 0.6 + norm_darkness * 1.0
                fill = ui_cyan
                opacity = 0.75
        else:
            if norm_darkness > 0.55:
                radius = 1.2 + (norm_darkness ** 1.3) * 1.8
                fill = "#4C1D95"
                opacity = 0.95
            elif norm_darkness > 0.35:
                radius = 0.9 + norm_darkness * 1.3
                fill = "#6D28D9"
                opacity = 0.85
            else:
                radius = 0.6 + norm_darkness * 1.0
                fill = "#7C3AED"
                opacity = 0.70
                
        portrait_circles.append(
            f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{radius:.2f}" fill="{fill}" opacity="{opacity:.2f}" />'
        )
        
    portrait_svg_group = "\n      ".join(portrait_circles)
    python_content = create_python_state(ui_cyan, accent_violet, panel_bg, text_primary)
    ai_content = create_ai_state(ui_cyan, accent_violet, success_green, header_bg, panel_bg, text_primary)
    code_content = create_code_state(ui_cyan, accent_violet, success_green, panel_bg, text_primary)
    
    # CSS Styling
    if mode == "debug" or forced_state is not None:
        # Static mode: explicit opacity/display for debugging
        op_portrait = "1" if forced_state == "portrait" else "0"
        op_python = "1" if forced_state == "python" else "0"
        op_ai = "1" if forced_state == "ai" else "0"
        op_code = "1" if forced_state == "code" else "0"
        
        disp_portrait = "inline" if forced_state == "portrait" else "none"
        disp_python = "inline" if forced_state == "python" else "none"
        disp_ai = "inline" if forced_state == "ai" else "none"
        disp_code = "inline" if forced_state == "code" else "none"
        
        css_rules = f'''
      #portrait-state {{ opacity: {op_portrait}; display: {disp_portrait}; }}
      #python-state {{ opacity: {op_python}; display: {disp_python}; }}
      #ai-state {{ opacity: {op_ai}; display: {disp_ai}; }}
      #code-state {{ opacity: {op_code}; display: {disp_code}; }}
        '''
    else:
        # Animated mode: Opacity-only 16-second infinite loop (NO transform, NO display:none)
        css_rules = '''
      #portrait-state { opacity: 1; animation: anim-portrait 16s ease-in-out infinite; }
      #python-state { opacity: 0; animation: anim-python 16s ease-in-out infinite; }
      #ai-state { opacity: 0; animation: anim-ai 16s ease-in-out infinite; }
      #code-state { opacity: 0; animation: anim-code 16s ease-in-out infinite; }
      
      /* 
         16s Infinite Loop Schedule:
         0% - 22%  (0s - 3.5s)   : Portrait visible
         25% - 42% (4.0s - 6.7s)  : Python visible
         45% - 62% (7.2s - 9.9s)  : AI/ML visible
         65% - 82% (10.4s - 13.1s): Code visible
         85% - 100%(13.6s - 16.0s): Portrait visible
      */
      
      @keyframes anim-portrait {
        0%, 22% { opacity: 1; }
        25%, 82% { opacity: 0; }
        85%, 100% { opacity: 1; }
      }
      
      @keyframes anim-python {
        0%, 22% { opacity: 0; }
        25%, 42% { opacity: 1; }
        45%, 100% { opacity: 0; }
      }
      
      @keyframes anim-ai {
        0%, 42% { opacity: 0; }
        45%, 62% { opacity: 1; }
        65%, 100% { opacity: 0; }
      }
      
      @keyframes anim-code {
        0%, 62% { opacity: 0; }
        65%, 82% { opacity: 1; }
        85%, 100% { opacity: 0; }
      }
        '''

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" width="100%" height="100%">
  <defs>
    <!-- Strict Viewport ClipPath for VISUAL.MAP Graphics -->
    <clipPath id="portrait-clip">
      <rect x="{vp_x}" y="{vp_y}" width="{vp_w}" height="{vp_h}" rx="6" />
    </clipPath>

    <!-- Font Import & Styling -->
    <style><![CDATA[
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');
      
      .bg-canvas {{ fill: {bg_main}; }}
      .panel-bg {{ fill: {panel_bg}; stroke: {panel_border}; stroke-width: 1.5; rx: 12px; }}
      .header-bg {{ fill: {header_bg}; stroke: {header_border}; stroke-width: 1; }}
      
      .font-mono {{ font-family: 'Fira Code', ui-monospace, Menlo, Consolas, monospace; }}
      .font-sans {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; }}
      
      .txt-cyan {{ fill: {ui_cyan}; }}
      .txt-violet {{ fill: {accent_violet}; }}
      .txt-green {{ fill: {success_green}; }}
      .txt-primary {{ fill: {text_primary}; }}
      .txt-muted {{ fill: {text_muted}; }}
      .txt-dim {{ fill: {text_dim}; }}
      
      /* Pulse for LIVE indicator */
      @keyframes pulse-live {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.35; transform: scale(0.95); }}
      }}
      .live-dot {{ animation: pulse-live 2.2s ease-in-out infinite; transform-origin: center; }}
      
      {css_rules}
    ]]></style>
  </defs>

  <!-- Canvas Background -->
  <rect width="1180" height="610" class="bg-canvas" rx="16" />

  <!-- Terminal Header Bar -->
  <g transform="translate(0, 0)">
    <rect width="1180" height="46" class="header-bg" rx="16" />
    <rect y="30" width="1180" height="16" class="header-bg" />
    
    <!-- Window Control Buttons -->
    <circle cx="28" cy="23" r="6" fill="#FF5F56" />
    <circle cx="48" cy="23" r="6" fill="#FFBD2E" />
    <circle cx="68" cy="23" r="6" fill="#27C93F" />
    
    <!-- Terminal Title -->
    <text x="96" y="28" class="font-mono" font-size="13" font-weight="600">
      <tspan class="txt-cyan">pranav@github</tspan><tspan class="txt-muted">:</tspan><tspan class="txt-primary">~$ profile.sh --live</tspan>
    </text>
    
    <!-- LIVE Status Indicator -->
    <g transform="translate(1085, 23)">
      <circle cx="0" cy="0" r="4.5" fill="{success_green}" class="live-dot" />
      <text x="12" y="4" class="font-mono txt-green" font-size="11" font-weight="700" letter-spacing="1">LIVE</text>
    </g>
  </g>

  <!-- ================= LEFT PANEL: VISUAL.MAP ================= -->
  <g transform="translate(40, 70)">
    <!-- Panel Container -->
    <rect width="440" height="500" class="panel-bg" />
    
    <!-- Panel Header Bar -->
    <path d="M 0 12 C 0 5.373, 5.373 0, 12 0 L 428 0 C 434.627 0, 440 5.373, 440 12 L 440 38 L 0 38 Z" fill="{header_bg}" stroke="{panel_border}" stroke-width="1" />
    <text x="20" y="24" class="font-mono txt-cyan" font-size="12" font-weight="700" letter-spacing="1.5">◆ VISUAL.MAP</text>
    <text x="375" y="24" class="font-mono txt-muted" font-size="11">[SRC:PORTRAIT]</text>
  </g>

  <!-- Viewport Outline Box -->
  <rect x="{vp_x}" y="{vp_y}" width="{vp_w}" height="{vp_h}" fill="none" stroke="{leader_color}" stroke-width="1" stroke-dasharray="4 4" rx="6" />

  <!-- ALL VISUAL.MAP GRAPHICS (SINGLE CLIPPED PARENT GROUP) -->
  <g id="visual-content" clip-path="url(#portrait-clip)">
    
    <!-- 1. PORTRAIT STATE -->
    <g id="portrait-state">
      {portrait_svg_group}
    </g>
    
    <!-- 2. PYTHON STATE (Centered at {center_x}, {symbol_center_y}) -->
    <g id="python-state" transform="translate({center_x}, {symbol_center_y})">
      {python_content}
    </g>
    
    <!-- 3. AI / ML STATE (Centered at {center_x}, {symbol_center_y}) -->
    <g id="ai-state" transform="translate({center_x}, {symbol_center_y})">
      {ai_content}
    </g>
    
    <!-- 4. CODE STATE (Centered at {center_x}, {symbol_center_y}) -->
    <g id="code-state" transform="translate({center_x}, {symbol_center_y})">
      {code_content}
    </g>
    
  </g>

  <!-- Foreground Status Bar (Positioned cleanly below the portrait viewport at y=515) -->
  <g transform="translate(58, 515)">
    <rect width="404" height="37" fill="{header_bg}" rx="4" />
    <text x="14" y="23" class="font-mono txt-muted" font-size="11">MODE: ACTIVE</text>
    <text x="160" y="23" class="font-mono txt-violet" font-size="11" font-weight="600">STATE: SYSTEM.OK</text>
    <text x="345" y="23" class="font-mono txt-green" font-size="11" font-weight="600">60FPS</text>
  </g>

  <!-- ================= RIGHT PANEL: SYSTEM.INFO ================= -->
  <g transform="translate(510, 70)">
    <!-- Panel Container -->
    <rect width="630" height="500" class="panel-bg" />
    
    <!-- Panel Header Bar -->
    <path d="M 0 12 C 0 5.373, 5.373 0, 12 0 L 618 0 C 624.627 0, 630 5.373, 630 12 L 630 38 L 0 38 Z" fill="{header_bg}" stroke="{panel_border}" stroke-width="1" />
    <text x="20" y="24" class="font-mono txt-cyan" font-size="12" font-weight="700" letter-spacing="1.5">⚡ SYSTEM.INFO</text>
    <text x="525" y="24" class="font-mono txt-muted" font-size="11">[SYS:PARAMS]</text>

    <!-- Main Header -->
    <g transform="translate(30, 72)">
      <text x="0" y="0" class="font-sans txt-primary" font-size="28" font-weight="800" letter-spacing="1">PRANAV MISTRY</text>
      
      <!-- Handle Badge -->
      <rect x="0" y="12" width="135" height="24" fill="{header_bg}" stroke="{panel_border}" stroke-width="1" rx="12" />
      <text x="12" y="28" class="font-mono txt-cyan" font-size="12" font-weight="600">@Pranav-Mistry</text>
      
      <text x="150" y="28" class="font-sans txt-muted" font-size="13" font-weight="500">B.Tech CSE Student</text>
    </g>
    
    <!-- Separator Line -->
    <line x1="30" y1="120" x2="600" y2="120" stroke="{header_border}" stroke-width="1" stroke-dasharray="2 2" />

    <!-- Technical Profile Specifications Table -->
    <g transform="translate(30, 150)" class="font-mono" font-size="13">
      
      <!-- ROW 1: Role -->
      <g transform="translate(0, 0)">
        <text x="0" y="0" class="txt-cyan" font-weight="600">Role</text>
        <line x1="110" y1="-4" x2="230" y2="-4" stroke="{leader_color}" stroke-width="1" stroke-dasharray="2 4" />
        <text x="240" y="0" class="txt-primary" font-weight="500">B.Tech Computer Science &amp; Engineering Student</text>
      </g>
      
      <!-- ROW 2: Focus -->
      <g transform="translate(0, 32)">
        <text x="0" y="0" class="txt-cyan" font-weight="600">Focus</text>
        <line x1="110" y1="-4" x2="230" y2="-4" stroke="{leader_color}" stroke-width="1" stroke-dasharray="2 4" />
        <text x="240" y="0" class="txt-violet" font-weight="600">AI • Machine Learning • Software Development</text>
      </g>

      <!-- ROW 3: Status -->
      <g transform="translate(0, 64)">
        <text x="0" y="0" class="txt-cyan" font-weight="600">Status</text>
        <line x1="110" y1="-4" x2="230" y2="-4" stroke="{leader_color}" stroke-width="1" stroke-dasharray="2 4" />
        <text x="240" y="0" class="txt-green" font-weight="600">Building • Learning • Exploring</text>
      </g>

      <!-- Sub Separator -->
      <line x1="0" y1="82" x2="570" y2="82" stroke="{header_border}" stroke-width="1" />

      <!-- ROW 4: Languages -->
      <g transform="translate(0, 114)">
        <text x="0" y="0" class="txt-muted" font-weight="600">Languages</text>
        <line x1="110" y1="-4" x2="230" y2="-4" stroke="{leader_color}" stroke-width="1" stroke-dasharray="2 4" />
        <text x="240" y="0" class="txt-primary">Python <tspan class="txt-dim">•</tspan> Java <tspan class="txt-dim">•</tspan> JavaScript <tspan class="txt-dim">•</tspan> SQL</text>
      </g>

      <!-- ROW 5: Frontend -->
      <g transform="translate(0, 146)">
        <text x="0" y="0" class="txt-muted" font-weight="600">Frontend</text>
        <line x1="110" y1="-4" x2="230" y2="-4" stroke="{leader_color}" stroke-width="1" stroke-dasharray="2 4" />
        <text x="240" y="0" class="txt-primary">React <tspan class="txt-dim">•</tspan> HTML <tspan class="txt-dim">•</tspan> CSS</text>
      </g>

      <!-- ROW 6: Backend -->
      <g transform="translate(0, 178)">
        <text x="0" y="0" class="txt-muted" font-weight="600">Backend</text>
        <line x1="110" y1="-4" x2="230" y2="-4" stroke="{leader_color}" stroke-width="1" stroke-dasharray="2 4" />
        <text x="240" y="0" class="txt-primary">Flask <tspan class="txt-dim">•</tspan> Django</text>
      </g>

      <!-- ROW 7: Database -->
      <g transform="translate(0, 210)">
        <text x="0" y="0" class="txt-muted" font-weight="600">Database</text>
        <line x1="110" y1="-4" x2="230" y2="-4" stroke="{leader_color}" stroke-width="1" stroke-dasharray="2 4" />
        <text x="240" y="0" class="txt-primary">MySQL <tspan class="txt-dim">•</tspan> Firebase <tspan class="txt-dim">•</tspan> MongoDB</text>
      </g>

      <!-- ROW 8: AI / ML -->
      <g transform="translate(0, 242)">
        <text x="0" y="0" class="txt-muted" font-weight="600">AI / ML</text>
        <line x1="110" y1="-4" x2="230" y2="-4" stroke="{leader_color}" stroke-width="1" stroke-dasharray="2 4" />
        <text x="240" y="0" class="txt-violet" font-weight="600">Scikit-learn <tspan class="txt-dim">•</tspan> Pandas <tspan class="txt-dim">•</tspan> NumPy <tspan class="txt-dim">•</tspan> YOLO</text>
      </g>

      <!-- ROW 9: Tools -->
      <g transform="translate(0, 274)">
        <text x="0" y="0" class="txt-muted" font-weight="600">Tools</text>
        <line x1="110" y1="-4" x2="230" y2="-4" stroke="{leader_color}" stroke-width="1" stroke-dasharray="2 4" />
        <text x="240" y="0" class="txt-primary">Git <tspan class="txt-dim">•</tspan> GitHub <tspan class="txt-dim">•</tspan> VS Code <tspan class="txt-dim">•</tspan> Android Studio</text>
      </g>
    </g>

    <!-- Footer System Status -->
    <g transform="translate(30, 452)">
      <rect x="0" y="0" width="570" height="32" fill="{header_bg}" rx="4" />
      <circle cx="16" cy="16" r="4" fill="{success_green}" />
      <text x="28" y="20" class="font-mono txt-green" font-size="11" font-weight="600">SYSTEM ARCHITECTURE: STABLE</text>
      <text x="440" y="20" class="font-mono txt-muted" font-size="11">BUILD v2.4.0</text>
    </g>
  </g>

</svg>
'''
    return svg_content

def main():
    print("Generating production dark.svg...")
    dark_svg = generate_svg(theme="dark", mode="animated")
    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    print("Successfully created dark.svg")
        
    print("Generating production light.svg...")
    light_svg = generate_svg(theme="light", mode="animated")
    with open("light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    print("Successfully created light.svg")

if __name__ == "__main__":
    main()
