
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from tabulate import tabulate
import io
import sys
from contextlib import redirect_stdout
import pandas as pd

from matplotlib.offsetbox import OffsetImage
from matplotlib.offsetbox import AnnotationBbox
from PIL import Image
from mpl_toolkits.mplot3d import proj3d
import matplotlib.image as mpimg

# ---------- Outer MAgic GLYPHCACHE ----------
sector_img_cache = {}

def get_sector_img(path, max_size=256):
    if path not in sector_img_cache:
        img = Image.open(path)

        # resize while keeping aspect ratio
        img.thumbnail((max_size, max_size))

        sector_img_cache[path] = np.array(img)

    return sector_img_cache[path]
    
def draw_image_3d_frac(ax, img_path, xy_frac, zoom=0.2):
    img = get_sector_img(img_path)
    imagebox = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(
        imagebox,
        xy_frac,               # already in axes fraction
        xycoords='axes fraction',
        frameon=False,
        zorder=20
    )
    ax.add_artist(ab)

#--DOMAIN GLYPH CACHE--


sector_img_cache = {}

def get_sector_img(path, max_size=256):
    if path not in sector_img_cache:
        img = Image.open(path)

        # resize while keeping aspect ratio
        img.thumbnail((max_size, max_size))

        sector_img_cache[path] = np.array(img)

    return sector_img_cache[path]


def draw_image_3d(ax, img_path, xyz, zoom=1):
    img = get_sector_img(img_path)

    imagebox = OffsetImage(img, zoom=zoom)

    ab = AnnotationBbox(
        imagebox,
        (0.51, 0.51),   # center of axes
        xycoords='axes fraction',
        frameon=False,
        zorder=20
    )
    ax.add_artist(ab)
#------

# Mapping for range and range type
range_dict = {1: "self", 2: "touch", 5: "5 ft", 10: "10 ft", 15: "15 ft", 20: "20 ft", 25: "25 ft", 30: "30 ft", 35: "35 ft", 40: "40 ft",45: "45 ft", 50: "50 ft", 55: "55 ft", 60: "60 ft", 100: "100 ft", 120: "120 ft", 150: "150 ft", 200: "200 ft", 250: "250 ft", 300: "300 ft", 350: "350 ft", 400: "400 ft", 450: "450 ft", 500: "500 ft" }
rt_dict = {1: "self", 2: "touch", 3: "point", 4: "beam", 5: "cone", 6: "radial"}

# Dictionary mapping range/rt values → symbols
range_rt_symbol_dict = {
    # Ranges
    "self": "x",
    "touch": "○",
    "5 ft": r'$\cdot$',
    "10 ft": "—",
    "15 ft": r'$\dotminus$',
    "20 ft": "=",
    "25 ft": r'$\doteq$',
    "30 ft": r'$\equiv$',
    "35 ft":r'$\equiv\cdot$',
    "40 ft": r'$-/$',
    "45 ft": r'$-/\cdot$',
    "50 ft": r'$/$',
    "55 ft": r'$/\cdot$',
    "60 ft": r'$/-$',
    "65 ft": r'$/-\cdot$',
    "100 ft": "|",
    "120 ft": "|=",
    "150 ft": "|/",
    "200 ft": "||",
    "250 ft": "||/",
    "300 ft": "|||",
    "350 ft": "|||/",
    "400 ft": "||||",
    "450 ft": "||||/",
    "500 ft": r'$\setminus$',
    

    # Range Types
    "point": "●",
    "beam": "—",
    "radial": "●—",
    "cone": "<"
}

# ---------------- Helper functions ----------------
def orbital_radius(level, radius_step, min_inner):
    if level == 1:
        return max(radius_step, min_inner)
    return min_inner + (level - 1) * radius_step
    
def bezier_curve_3d(p0, p1, p2, n_points=50):
    t = np.linspace(0,1,n_points)
    curve = ((1-t)**2)[:,None]*p0 + (2*((1-t)*t))[:,None]*p1 + (t**2)[:,None]*p2
    return curve[:,0], curve[:,1], curve[:,2]

def draw_electron_connection(ax, p1, p2, n_lines=1, spacing=0.15, level = 1, sec1=None, sec2=None,
                             arch_factor=0.3, flip=True, quicken=0, chann=2, chann2=1, tick_len=0.5, vig=2, fiver=2):
    p1 = np.array(p1)
    p2 = np.array(p2)
    # ---- ENERGY → SPACING SCALE ----
    energy_scale = 1.0 + 0.35 * (level - 1)
    effective_spacing = spacing * energy_scale
    distance = np.linalg.norm(p2 - p1)
    arch_height = distance * arch_factor
    #offsets = [0] if n_lines == 1 else np.linspace(-(n_lines-1)/2*spacing, (n_lines-1)/2*spacing, n_lines)
    offsets = ([0] if n_lines == 1 else np.linspace(-(n_lines - 1) / 2 * effective_spacing, (n_lines - 1) / 2 * effective_spacing, n_lines))

    lines_drawn = 0
    used_quicken = 0
    cross_sector_extra = 0
    tick_count = chann2 if chann==1 else 0
    tick_count = min(tick_count, n_lines)

    for i, off in enumerate(offsets):
        is_red = quicken > used_quicken
        used_quicken += int(is_red)

        if sec1 == sec2:
            vec = p2 - p1
            if np.linalg.norm(vec[:2]) == 0:
                perp = np.array([1,0,0])
            else:
                perp = np.array([-vec[1], vec[0], 0])
            perp = perp / np.linalg.norm(perp) * off
            ax.plot([p1[0]+perp[0], p2[0]+perp[0]],
                    [p1[1]+perp[1], p2[1]+perp[1]],
                    [p1[2]+perp[2], p2[2]+perp[2]],
                    "-." if is_red else "-", color="black", linewidth= 1.5)
            # ---- Draw V-marker for VIG ----
            if vig == 1:
                # vector from second to first (arrow direction)
                direction = p1 - p2
                norm = np.linalg.norm(direction)
                if norm == 0:
                    direction = np.array([1,0,0])
                else:
                    direction /= norm
            
                # place the V slightly before the first electron
                arrow_pos = p1 - direction * 1.2  # adjust distance to scene scale
            
                # create two legs of the V at an angle (e.g., 30 degrees) to the connection
                angle_deg = 30
                angle_rad = np.radians(angle_deg)
            
                # find two perpendicular vectors to the direction
                if abs(direction[2]) < 0.9:
                    temp = np.array([0,0,1])
                else:
                    temp = np.array([1,0,0])
                perp1 = np.cross(direction, temp)
                perp1 /= np.linalg.norm(perp1)
                perp2 = np.cross(direction, perp1)
                perp2 /= np.linalg.norm(perp2)
            
                # V size
                V_size = 1.0
            
                # rotate perp1 and perp2 by angle_rad around direction to form V legs
                leg1 = np.cos(angle_rad)*(-direction) + np.sin(angle_rad)*perp1
                leg2 = np.cos(angle_rad)*(-direction) + np.sin(angle_rad)*(-perp1)
            
                # scale to V size
                leg1 *= V_size
                leg2 *= V_size
            
                # draw V
                ax.plot([arrow_pos[0], arrow_pos[0] + leg1[0]],
                        [arrow_pos[1], arrow_pos[1] + leg1[1]],
                        [arrow_pos[2], arrow_pos[2] + leg1[2]],
                        color="black", linewidth=2, zorder=12)
            
                ax.plot([arrow_pos[0], arrow_pos[0] + leg2[0]],
                        [arrow_pos[1], arrow_pos[1] + leg2[1]],
                        [arrow_pos[2], arrow_pos[2] + leg2[2]],
                        color="black", linewidth=2, zorder=12)
            
            
            if fiver == 1:
                # vector from first to second (arrow direction)
                direction = p2 - p1
                norm = np.linalg.norm(direction)
                if norm == 0:
                    direction = np.array([1,0,0])
                else:
                    direction /= norm
            
                # place the V slightly before the second electron
                arrow_pos = p2 - direction * 0.5  # adjust distance to scene scale
            
                # create two legs of the V at an angle (e.g., 30 degrees) to the connection
                angle_deg = 30
                angle_rad = np.radians(angle_deg)
            
                # find two perpendicular vectors to the direction
                if abs(direction[2]) < 0.9:
                    temp = np.array([0,0,1])
                else:
                    temp = np.array([1,0,0])
                perp1 = np.cross(direction, temp)
                perp1 /= np.linalg.norm(perp1)
                perp2 = np.cross(direction, perp1)
                perp2 /= np.linalg.norm(perp2)
            
                # V size
                V_size = 0.8
            
                # rotate perp1 and perp2 by angle_rad around direction to form V legs
                leg1 = np.cos(angle_rad)*(-direction) + np.sin(angle_rad)*perp1
                leg2 = np.cos(angle_rad)*(-direction) + np.sin(angle_rad)*(-perp1)
            
                # scale to V size
                leg1 *= V_size
                leg2 *= V_size
            
                # draw V
                ax.plot([arrow_pos[0], arrow_pos[0] + leg1[0]],
                        [arrow_pos[1], arrow_pos[1] + leg1[1]],
                        [arrow_pos[2], arrow_pos[2] + leg1[2]],
                        color="black", linewidth=2, zorder=12)
            
                ax.plot([arrow_pos[0], arrow_pos[0] + leg2[0]],
                        [arrow_pos[1], arrow_pos[1] + leg2[1]],
                        [arrow_pos[2], arrow_pos[2] + leg2[2]],
                        color="black", linewidth=2, zorder=12)

            if i < tick_count:
                mid = (p1 + p2)/2 + perp
                tangent = vec / np.linalg.norm(vec)
                perp3 = np.cross(tangent, np.array([0,0,1.0]))
                if np.linalg.norm(perp3)<1e-6:
                    perp3 = np.cross(tangent, np.array([0,1,0]))
                perp3 /= np.linalg.norm(perp3)
                tick1 = mid + perp3*(tick_len/2)
                tick2 = mid - perp3*(tick_len/2)
                ax.plot([tick1[0], tick2[0]], [tick1[1], tick2[1]], [tick1[2], tick2[2]], color="black", linewidth=2)

        # if curved
        else:
            dir_xy = p2[:2] - p1[:2]
            perp_xy = np.array([-dir_xy[1], dir_xy[0]])
            if flip:
                perp_xy = -perp_xy
            if np.linalg.norm(perp_xy) != 0:
                perp_xy = perp_xy / np.linalg.norm(perp_xy)
            cp = (p1 + p2)/2 + np.append(perp_xy * arch_height + perp_xy*off, 0)
            x, y, z = bezier_curve_3d(p1, cp, p2)
            ax.plot(x, y, z,"-." if is_red else "-", color="black", linewidth= 1.5)
            # --- V for vig: should sit near the p1 end and point TOWARD p1 ---
            if vig == 1:
                # pick an index near p1 (15% along the curve)
                idx = max(1, int(len(x) * 0.1))
                if idx >= len(x) - 1:
                    idx = len(x) // 2
            
                V_pos = np.array([x[idx], y[idx], z[idx]])
            
                # compute local tangent (next - prev)
                tangent = np.array([x[idx+1] - x[idx-1],
                                    y[idx+1] - y[idx-1],
                                    z[idx+1] - z[idx-1]])
                tnorm = np.linalg.norm(tangent)
                if tnorm == 0:
                    tangent = np.array([1.0, 0.0, 0.0])
                else:
                    tangent /= tnorm
            
                # direction for vig should point TOWARD p1 -> use -tangent
                direction = tangent
            
                # perpendicular for V spread
                perp = np.cross(direction, np.array([0,0,1.0]))
                if np.linalg.norm(perp) < 1e-6:
                    perp = np.cross(direction, np.array([0,1,0.0]))
                perp /= np.linalg.norm(perp)
            
                # V geometry
                angle = np.radians(30)
                size  = 0.8
            
                leg1 = direction * np.cos(angle) + perp * np.sin(angle)
                leg2 = direction * np.cos(angle) - perp * np.sin(angle)
                leg1 *= size
                leg2 *= size
            
                # tiny offset toward p1 so the V sits slightly off the curve
                bond_len = np.linalg.norm(p2 - p1)
                offset = 0.05 * bond_len
                V_pos = V_pos + direction * offset
            
                # draw the V legs
                ax.plot([V_pos[0], V_pos[0] + leg1[0]],
                        [V_pos[1], V_pos[1] + leg1[1]],
                        [V_pos[2], V_pos[2] + leg1[2]],
                        color='black', linewidth=2)
            
                ax.plot([V_pos[0], V_pos[0] + leg2[0]],
                        [V_pos[1], V_pos[1] + leg2[1]],
                        [V_pos[2], V_pos[2] + leg2[2]],
                        color='black', linewidth=2)

                
            if fiver == 1:
                # pick a point near p2 end of curve (85% toward end)
                idx = int(len(x)*0.85)
                V_pos = np.array([x[idx], y[idx], z[idx]])
            
                # tangent direction at the V point 
                direction = np.array([x[idx+1]-x[idx-1],
                                      y[idx+1]-y[idx-1],
                                      z[idx+1]-z[idx-1]])
                direction /= np.linalg.norm(direction)
            
                # perpendicular basis
                perp = np.cross(direction, np.array([0,0,1]))
                if np.linalg.norm(perp) < 1e-6:
                    perp = np.cross(direction, np.array([0,1,0]))
                perp /= np.linalg.norm(perp)
            
                # V angle and size
                angle = np.radians(30)
                size  = 0.8
            
                leg1 = -direction*np.cos(angle) + perp*np.sin(angle)
                leg2 = -direction*np.cos(angle) - perp*np.sin(angle)
                leg1 *= size
                leg2 *= size
            
                # draw V
                ax.plot([V_pos[0], V_pos[0]+leg1[0]],
                        [V_pos[1], V_pos[1]+leg1[1]],
                        [V_pos[2], V_pos[2]+leg1[2]],
                        color='black', linewidth=2)
            
                ax.plot([V_pos[0], V_pos[0]+leg2[0]],
                        [V_pos[1], V_pos[1]+leg2[1]],
                        [V_pos[2], V_pos[2]+leg2[2]],
                        color='black', linewidth=2)


            if i < tick_count:
                mid_idx = len(x)//2
                tangent = np.array([x[-1]-x[0], y[-1]-y[0], z[-1]-z[0]])
                tangent /= np.linalg.norm(tangent)
                perp3 = np.cross(tangent, np.array([0,0,1]))
                if np.linalg.norm(perp3)<1e-6:
                    perp3 = np.cross(tangent, np.array([0,1,0]))
                perp3 /= np.linalg.norm(perp3)
                tick1 = np.array([x[mid_idx], y[mid_idx], z[mid_idx]]) + perp3*(tick_len/2)
                tick2 = np.array([x[mid_idx], y[mid_idx], z[mid_idx]]) - perp3*(tick_len/2)
                ax.plot([tick1[0], tick2[0]], [tick1[1], tick2[1]], [tick1[2], tick2[2]], color="black", linewidth=2)
        
        lines_drawn += 1

    if sec1 != sec2:
        cross_sector_extra = 1
        lines_drawn += 1

    
    
                       

    return {'lines_drawn': lines_drawn, 'cross_sector_extra': cross_sector_extra, 'used_quicken': used_quicken}

def wedge_to_3d(wedge, z=0):
    verts = wedge.get_verts()
    xs, ys = verts[:,0], verts[:,1]
    zs = np.zeros_like(xs) + z
    return xs, ys, zs

def parse_range_value(r):
    if isinstance(r, str):
        if r.lower() in ["self","touch"]:
            return 1
        elif "ft" in r:
            return int(r.replace(" ft",""))
    return int(r)

def calculate_range_increase_charge(base_range_ft, range_increase):
    if base_range_ft <= 20:
        return range_increase * 1
    elif 20 < base_range_ft <= 30:
        return range_increase * 2
    elif 30 < base_range_ft < 100:
        return range_increase * 3
    else:
        return range_increase * 5

def level_size_scale(level, base=1.0, factor=0):
    """
    Scales size by energy level.
    level: electron energy level
    base: base size at min_level
    factor: growth per level
    """
    if level == 1:
        base = 1.5
        return base
    else:
        return base * (1 + factor * level)


def draw_modifier_shape(ax, shape, center, size=1.0, color='black', level=1):
    x0, y0, z0 = center
    z = z0 + 0.5  # lift shape above electron marker
    size = level_size_scale(level, base=size, factor=1)
    if shape == "square":
        #half = size / 1.5
        half = size * 1.2
        corners = np.array([
            [x0 - half, y0 - half, z],
            [x0 + half, y0 - half, z],
            [x0 + half, y0 + half, z],
            [x0 - half, y0 + half, z],
            [x0 - half, y0 - half, z]  # close the square
        ])
        ax.plot(corners[:, 0], corners[:, 1], corners[:, 2], color=color, linewidth=2.5, zorder = 13)
    elif shape == "double_square":
        #half = size / 1
        half = size * 2
        #half2 = half / 1.2
        half2 = size * 1.7
        
        corners = np.array([
            [x0 - half, y0 - half, z],
            [x0 + half, y0 - half, z],
            [x0 + half, y0 + half, z],
            [x0 - half, y0 + half, z],
            [x0 - half, y0 - half, z]  # close the square
        ])
        corners2 = np.array([
            [x0 - half2, y0 - half2, z],
            [x0 + half2, y0 - half2, z],
            [x0 + half2, y0 + half2, z],
            [x0 - half2, y0 + half2, z],
            [x0 - half2, y0 - half2, z]  # close the square
        ])
        ax.plot(corners[:, 0], corners[:, 1], corners[:, 2], color=color, linewidth=1.5,zorder = 13)
        ax.plot(corners2[:, 0], corners2[:, 1], corners2[:, 2], color=color, linewidth=1.5,zorder = 13)
    elif shape == "triangle":
        half = size*3 
        y_offset = half * 0.35
        corners = np.array([
            [x0,        y0 - half- y_offset+0.2, z],        # top
            [x0 - half , y0 + half - y_offset, z],        # bottom left
            [x0 + half, y0 + half - y_offset, z],        # bottom right
            [x0,        y0 - half- y_offset+0.2, z]         # close triangle
        ])
        ax.plot(corners[:, 0], corners[:, 1], corners[:, 2], color=color, linewidth=1.5, zorder=6)
    elif shape == "double_triangle":
        half = size 
        y_offset = half * 0.35 
        corners = np.array([
            [x0,        y0 - half- y_offset+0.2, z],        # top
            [x0 - half , y0 + half - y_offset, z],        # bottom left
            [x0 + half, y0 + half - y_offset, z],        # bottom right
            [x0,        y0 - half- y_offset+0.2, z]         # close triangle
        ])
        half2 = size*1.5 
        y_offset2 = half2 * 0.35 *1.5 
        corners2 = np.array([
            [x0,        y0 - half2- y_offset2+0.2, z],        # top
            [x0 - half2 , y0 + half2 - y_offset2, z],        # bottom left
            [x0 + half2, y0 + half2 - y_offset2, z],        # bottom right
            [x0,        y0 - half2- y_offset2+0.2, z]         # close triangle
        ])
        ax.plot(corners[:, 0], corners[:, 1], corners[:, 2], color=color, linewidth=1.5, zorder=13)
        ax.plot(corners2[:, 0], corners2[:, 1], corners2[:, 2], color=color, linewidth=1.5, zorder=13)
    elif shape == "circle":
        theta = np.linspace(0, 2 * np.pi, 50)
        xs = x0 + (size*2) * np.cos(theta)
        ys = y0 + (size*2) * np.sin(theta)
        zs = np.ones_like(xs) * z
        ax.plot(xs, ys, zs, color=color, linewidth=1.5)
        
    elif shape == "diamond":
        half = size / 0.4
        corners = np.array([
            [x0,        y0 + half, z],  # top
            [x0 + (0.75*half), y0,        z],  # right
            [x0,        y0 - half, z],  # bottom
            [x0 - (0.75*half), y0,        z],  # left
            [x0,        y0 + half, z]   # close the diamond
        ])
        ax.plot(corners[:, 0], corners[:, 1], corners[:, 2], color=color, linewidth=1.5,zorder = 13)
    elif shape == "double_diamond":
        half = size / 0.25
        half2 = size / 0.5   # inner diamond scale factor
    
        # inner diamond
        corners = np.array([
            [x0,                 y0 + half2, z],   # top
            [x0 + 0.75*half2,     y0,        z],   # right
            [x0,                 y0 - half2, z],   # bottom
            [x0 - 0.75*half2,     y0,        z],   # left
            [x0,                 y0 + half2, z]
        ])
    
        # outer diamond
        corners2 = np.array([
            [x0,                 y0 + half, z],
            [x0 + 0.75*half,    y0,         z],
            [x0,                 y0 - half, z],
            [x0 - 0.75*half,    y0,         z],
            [x0,                 y0 + half, z]
        ])
    
        ax.plot(
            corners[:, 0],
            corners[:, 1],
            corners[:, 2],
            color=color,
            linewidth=1.5,
            zorder=13
        )
    
        ax.plot(
            corners2[:, 0],
            corners2[:, 1],
            corners2[:, 2],
            color=color,
            linewidth=1.5,
            zorder=13
        )
    elif shape == "diamond_triangle":
        # --- triangle geometry ---
        d = size * 3        # distance between diamonds
        h = d * np.sqrt(3)/2 
    
        centers = [
            (x0,       y0 + h, z),   # top
            (x0 - d/2, y0 - h/2, z),   # bottom left
            (x0 + d/2, y0 - h/2, z)    # bottom right
        ]
    
        half = size*1.5 # / 1.5  
    
        for cx, cy, cz in centers:
            corners = np.array([
                [cx,               cy + half, cz],  # top
                [cx + 0.75*half,   cy,        cz],  # right
                [cx,               cy - half, cz],  # bottom
                [cx - 0.75*half,   cy,        cz],  # left
                [cx,               cy + half, cz]   # close
            ])
            ax.plot(
                corners[:, 0],
                corners[:, 1],
                corners[:, 2],
                color=color,
                linewidth=1.5,
                zorder=13
            )
    elif shape == "ripple":
        horn_radius = size * 2.5
        horn_offset = size * -0.2   # lifts horns above circle center
    
        theta_h = np.linspace(0, np.pi, 50)  # semicircle facing UP
        hx = x0 + horn_radius * np.cos(theta_h)
        hy = y0 + horn_offset + horn_radius * np.sin(theta_h)
        hz = np.ones_like(hx) * z
    
        ax.plot(hx, hy, hz, color=color, linewidth=1.5, zorder=14)





# ---------------- Main function ----------------
def draw_atom_words_from_dict(words_list, words_dict, modifiers_dict=None, modifiers_to_apply=None,
                              sector_labels=None, tilt=False, alt=90, azim=90, quicken=0, range_increase_input=0, range_type_change = 0):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        if sector_labels is None:
            #sector_labels = {1:"↙️",2:"⬇️",3:"↘️",4:"↗️",5:"⬆️",6:"↖️"}
            sector_labels = {1:"GlyphGraphics/End.png",2:"GlyphGraphics/Death.png",3:"GlyphGraphics/Witchcraft.png",4:"GlyphGraphics/Shamanism.png",5:"GlyphGraphics/Druidism.png",6:"GlyphGraphics/Ley.png"}
    
        allowed_sectors = sorted({words_dict[word]["section"] for word in words_list})
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("tan")
        plt.axis("off")
        sector_angle = np.pi/3
        theta_full = np.linspace(0, 2*np.pi, 500)
        all_ranges = [] 
    
        # Nucleus
        first_word = words_list[0]
        first_sec = words_dict[first_word]["section"]
        nucleus_label = sector_labels.get(first_sec, str(first_sec))
        ax.scatter(0,0,0,marker="h", facecolors='tan', edgecolors='black', linewidths=1.5, s=2500)
        img_path = sector_labels.get(first_sec)

        if img_path:
            draw_image_3d(ax, img_path, (0, 0, 0.25), zoom=0.25)
        else:
            ax.text(0,0,0.2,str(first_sec), color="black",
                    ha="center", va="center", fontsize=20)
        #ax.text(0,0,0.2,nucleus_label,color="black",ha="center",va="center", fontsize=20,fontweight="bold")
    
        # Radius setup
        max_level = max([words_dict[word]["level"] for word in words_list])
        NUCLEUS_RADIUS = 5  # matches your hex marker scale
        CLEARANCE = 10
        MIN_INNER_RADIUS = NUCLEUS_RADIUS + CLEARANCE
        radius_step = 5.0
        max_radius = orbital_radius(max_level, radius_step, MIN_INNER_RADIUS)
    
        # Radial lines + sector labels
        label_radius = max_radius + 0.7
        for i in range(6):
            angle = i*sector_angle
            x = max_radius*np.cos(angle)
            y = max_radius*np.sin(angle)
            ax.plot([0,x],[0,y],[0,0],color="black",linestyle="--",linewidth=1,alpha=0.5)
            label_angle = angle + sector_angle/2
            lx = label_radius*np.cos(label_angle)
            ly = label_radius*np.sin(label_angle)
            img_path_sector = sector_labels.get(i+1)

            if img_path_sector:
                draw_image_3d_frac(ax, img_path_sector, (lx,ly, 20), zoom=0.25)
            else:
                ax.text(ly,ly,20,str(i+1), color="black",
                        ha="center", va="center", fontsize=20)
            
            #ax.text(lx,ly,20,sector_labels.get(i+1,str(i+1)),color="black",ha="center",va="center",fontsize=20, alpha=0.5)
    
        # Shade allowed sectors
        for sec in allowed_sectors:
            start_deg = (sec-1)*60
            end_deg = sec*60
            wedge = Wedge((0,0), r=max_radius+0.5, theta1=start_deg, theta2=end_deg, facecolor="black", alpha=0.1)
            xs, ys, zs = wedge_to_3d(wedge)
            ax.plot_trisurf(xs, ys, zs, color="teal", alpha=0.12)
    
        # Draw orbitals
    
        for L in range(1, max_level + 1):
            r = orbital_radius(L, radius_step, MIN_INNER_RADIUS)
            tilt_angle = L*12*np.pi/180 if tilt else 0
            x = r*np.cos(theta_full)
            y = r*np.sin(theta_full)*np.cos(tilt_angle)
            z = r*np.sin(theta_full)*np.sin(tilt_angle)
            ax.plot(x, y, z, linestyle="-", color="black", alpha=0.15)
    
        # Electron positions
        electron_positions = {}
        grouped = {}
        rtcEnergy = 0
        for word in words_list:
            info = words_dict[word]
            key = (info["level"], info["section"])
            grouped.setdefault(key, []).append((word, info))
    
        for (level, sec), words_in_group in grouped.items():
            r = orbital_radius(level, radius_step, MIN_INNER_RADIUS)
            tilt_angle = level*12*np.pi/180 if tilt else 0
            x = r*np.cos(theta_full)
            y = r*np.sin(theta_full)*np.cos(tilt_angle)
            z = r*np.sin(theta_full)*np.sin(tilt_angle)
            ax.plot(x, y, z, linestyle="-", color="black", alpha=0.3)
    
            n = len(words_in_group)
            sec_start = (sec-1)*sector_angle
            sec_center = sec_start + sector_angle/2
            angles = [sec_center] if n==1 else np.linspace(sec_center - 0.45, sec_center + 0.45, n)
            
    
            for (word, info), angle in zip(words_in_group, angles):
                xe = r*np.cos(angle)
                ye = r*np.sin(angle)*np.cos(tilt_angle)
                ze = r*np.sin(angle)*np.sin(tilt_angle)
                ax.scatter(xe, ye, ze, s=800, facecolors='tan', edgecolors='black')
                ax.text(xe, ye, ze+0.2, word, color="black", ha="center", va="center", fontsize=10, zorder=10)
    
                # --- RANGE + RT TEXT ABOVE/BELOW ELECTRON ---
                
                if not word.endswith(" EN"):
                    rng_num = info.get("range",0)*(range_increase_input+1)
                    rng_def=range_dict.get(rng_num)
                    print("Range with Mods:",rng_def)
                    all_ranges.append(rng_def)
                else:
                    rng_num = info.get("range",0)
                    all_ranges.append(rng_num)
                    
                
    
                rt_=info.get("rt",0) 
                #print(rt_)
                rt_chann = info.get("chann",2)
                MAX_RT = max(rt_dict.keys())
                if rt_ == 0:
                    rt_num = 0
                else:
                    rt_num  = min(rt_ + range_type_change, MAX_RT)
                #rt_num = rt_+ range_type_change
                
                    
                #print(rt_num)
                rng_def=range_dict.get(rng_num)
                rt_def=rt_dict.get(rt_num)
                #print(rng_def)
                #if range_increase_input > 0:
                rng_symbol = range_rt_symbol_dict.get(rng_def, "")
                rt_symbol = range_rt_symbol_dict.get(rt_def, "")
                #print(rng_symbol)
                #print(rt_symbol)
               # ax.text(xe, ye-0.1, ze+0.5, rng_symbol, color="black", ha="center", va="bottom", fontsize=9, zorder = 11)
               # ax.text(xe, ye+0.2, ze-0.5, rt_symbol, color="black", ha="center", va="top", fontsize=5, zorder = 11)
    
                # IMPORTANT FIX: use a copy of info
                electron_positions[word] = {
                    'pos': (xe, ye, ze),
                    'sector': sec,
                    'level': level,
                    'chann': info.get("chann",2),
                    'chann2': info.get("2chann",1),
                    'info': info.copy()
                }
                #rtcEnergy = 0
                if not word.endswith(" EN"):
                    if rt_ == 4 and range_type_change == 1:
                        rtcEnergy = 1
                    elif rt_ == 4 and range_type_change == 2:
                        rtcEnergy = 4
                    elif rt_ == 3 and range_type_change == 1:
                        rtcEnergy = 1
                    elif rt_ == 3 and range_type_change == 2:
                        rtcEnergy = 2
                    elif rt_ == 3 and rt_chann == 1 and range_type_change == 3:
                        rtcEnergy = 4
                    elif rt_ == 3 and range_type_change == 3:
                        rtcEnergy = 5
                    elif rt_ == 5 and range_type_change == 1:
                        rtcEnergy = 3
                    else:
                        rtcEnergy = 0
                #print(rtcEnergy)
    
    
        # ---------------- Apply Modifiers ----------------
        modAP = 0
        modEnergy = 0
        if modifiers_dict and modifiers_to_apply:
            for mod_key in modifiers_to_apply:
                mod = modifiers_dict.get(mod_key, None)
                if not mod:
                    continue
                targets = mod.get("appto", [])
                rt_over = mod.get("rt_over", 0)
                for target_word in targets:
                    if target_word in electron_positions:
                        print("Modifier", mod_key, ":",mod.get("comment", []))
                        pos = electron_positions[target_word]['pos']
                        level = electron_positions[target_word]['level']
                        draw_modifier_shape(ax, mod["shape"], pos, size=mod.get("size",2.0),level = level)
                        # Update AP/energy in word info
                        modAP += mod.get("AP",0)
                        modEnergy += mod.get("energy",0)
                        electron_positions[target_word]['info']['AP'] += mod.get("AP",0)
                        electron_positions[target_word]['level'] += mod.get("energy",0)
                        # ---- 🔥 RT + RANGE OVERRIDE LOGIC ---
                        if rt_over == 1:
                            electron_positions[target_word]['info']['rt'] = 3
                            electron_positions[target_word]['info']['range'] = 20
        # ---------------- DRAW RT + RANGE SYMBOLS (POST-MOD) ----------------
        for word, e in electron_positions.items():
            info = e['info']
            xe, ye, ze = e['pos']
        
            # ---- RANGE ----
            if not word.endswith(" EN"):
                rng_num = info.get("range", 0) * (range_increase_input + 1)
            else:
                rng_num = info.get("range", 0)
        
            rng_def = range_dict.get(rng_num)
            rng_symbol = range_rt_symbol_dict.get(rng_def, "")
        
            # ---- RT ----
            rt_ = info.get("rt", 0)
            MAX_RT = max(rt_dict.keys())
        
            if rt_ == 0:
                rt_num = 0
            else:
                rt_num = min(rt_ + range_type_change, MAX_RT)
        
            rt_def = rt_dict.get(rt_num)
            rt_symbol = range_rt_symbol_dict.get(rt_def, "")
        
            # ---- DRAW ----
            ax.text(
                xe, ye - 0.1, ze + 0.5,
                rng_symbol,
                color="black",
                ha="center",
                va="bottom",
                fontsize=9,
                zorder=11
            )
        
            ax.text(
                xe, ye + 0.2, ze - 0.5,
                rt_symbol,
                color="black",
                ha="center",
                va="top",
                fontsize=5,
                zorder=11
            )

                        
    
        # ---------------- Range Increase Mini-Orbitals ----------------
        if range_increase_input > 0:
            base_range_ft = parse_range_value(words_dict[first_word].get("range","self"))
            added_energy_cost = calculate_range_increase_charge(base_range_ft, range_increase_input)
            r_first = orbital_radius(electron_positions[first_word]['info']['level'],radius_step,MIN_INNER_RADIUS)
            for i in range(added_energy_cost):
                r = r_first - (i+1)*0.3
                tilt_angle = 0
                x = r*np.cos(theta_full)
                y = r*np.sin(theta_full)*np.cos(tilt_angle)
                z = r*np.sin(theta_full)*np.sin(tilt_angle)
                ax.plot(x, y, z, linestyle="-", color="black", alpha=0.2)
        else:
            added_energy_cost = 0
    
    
        # ---------------- AP & Energy Table ----------------
        table = []
        total_base_AP = total_cross_AP = total_base_energy = total_cross_energy = 0
        remaining_quicken = quicken
    
        # Nucleus → first electron
        first_electron = electron_positions[first_word]
        conn = draw_electron_connection(ax, (0,0,0), first_electron['pos'],
                                        n_lines=first_electron['info'].get("AP",1),
                                        spacing=1,
                                        level = first_electron['info']['level'],
                                        sec1=first_sec,
                                        sec2=first_electron['sector'],
                                        arch_factor=0.15, flip=True,
                                        quicken=remaining_quicken,
                                        chann=first_electron['chann'],
                                        chann2=first_electron['chann2'],
                                        vig=first_electron['info'].get("vig",0),
                                        fiver=first_electron['info'].get("fiver",0))
        remaining_quicken = max(0, remaining_quicken - conn['used_quicken'])
        base_AP = conn['lines_drawn'] - conn['cross_sector_extra']
        cross_AP = conn['cross_sector_extra']
        base_energy = first_electron['level']
        cross_energy = cross_AP
        total_base_AP += base_AP
        total_cross_AP += cross_AP
        total_base_energy += base_energy
        total_cross_energy += cross_energy
        total_base_energy += added_energy_cost
    
        table.append([
            "Parent Domain",
            first_word,
            base_AP,
            base_energy,
            cross_AP,
            cross_energy,
            sector_labels.get(first_electron.get("sector","N/A"), str(first_electron['info'].get("sector","N/A"))),
            range_dict.get(first_electron['info'].get("range","N/A"), str(first_electron['info'].get("range","N/A"))),
            rt_dict.get(first_electron['info'].get("rt","N/A"), str(first_electron['info'].get("rt","N/A"))),
            first_electron['info'].get("comment",""),
            "Yes" if first_electron['chann']==1 else "No",
            "None" if first_electron['chann']==2 else first_electron['info'].get("2chann","1")
        ])
    
        # Electron → electron
        for idx, word in enumerate(words_list):
            p1 = electron_positions[word]['pos']
            sec1 = electron_positions[word]['sector']
            level1 = electron_positions[word]['level']
            targets = words_dict[word].get("targets", [])
            if not targets and idx+1 < len(words_list):
                targets = [words_list[idx+1]]
    
            for t in targets:
                if t not in electron_positions:
                    continue
                target = electron_positions[t]
                conn = draw_electron_connection(ax, p1, target['pos'],
                                               n_lines=target['info'].get("AP",1),
                                               spacing=1,
                                               level = target['info']['level'],
                                               sec1=sec1, sec2=target['sector'],
                                               arch_factor=0.2, flip=True,
                                               quicken=remaining_quicken,
                                               chann=target['chann'],
                                               chann2=target['chann2'],
                                               vig=target['info'].get("vig",0),
                                               fiver=target['info'].get("fiver",0))
                remaining_quicken = max(0, remaining_quicken - conn['used_quicken'])
                base_AP = conn['lines_drawn'] - conn['cross_sector_extra']
                cross_AP = conn['cross_sector_extra']
                base_energy = 0 if (level1==target['level'] and sec1==target['sector']) else abs(target['level']-level1)
                cross_energy = cross_AP 
                total_base_AP += base_AP
                total_cross_AP += cross_AP
                total_base_energy += base_energy
                total_cross_energy += cross_energy
                if target['info'].get("over",0) == 1:
                    total_base_energy = total_base_energy + 1
                    total_base_AP = total_base_AP - 1
                elif target['info'].get("over",0) == 5:
                    total_base_energy = total_base_energy + 5
                    total_base_AP = total_base_AP - 1
                elif target['info'].get("over",0) == -1:
                    total_base_energy = total_base_energy
                    total_base_AP = total_base_AP - 1
    
                else:
                    total_base_energy = total_base_energy
                    total_base_AP = total_base_AP
    
                table.append([
                    word,
                    t,
                    base_AP,
                    base_energy,
                    cross_AP,
                    cross_energy,
                    sector_labels.get(target.get("sector","N/A"), str(target['info'].get("sector","N/A"))),
                    range_dict.get(target['info'].get("range","N/A"), str(target['info'].get("range","N/A"))),
                    rt_dict.get(target['info'].get("rt","N/A"), str(target['info'].get("rt","N/A"))),
                    target['info'].get("comment",""),
                    "Yes" if target['chann']==1 else "No",
                    "None" if target['chann']==2 else target['info'].get("2chann","1")
                ])       
    
        # ---------------- Print totals ----------------

        if all(r in (0, None) for r in all_ranges):
            print("**SPELL IS NOT FEASIBLE: NO RANGE**")
        #print(all_ranges)
        
    
        total_AP = total_base_AP + total_cross_AP 
        total_energy = total_base_energy + total_cross_energy +rtcEnergy
    
        
        
        if quicken > 0:
            print(f"TOTAL AP: {total_AP-quicken} (quicken applied)")
            print("TOTAL ENERGY:", total_energy*2*quicken,"(quicken applied)")
            
            
        else:
            print("TOTAL AP:", total_AP)
            print("TOTAL ENERGY:", total_energy)
        print ("AP from Mods:", modAP)
        print ("ENERGY from Mods:", modEnergy + rtcEnergy)
        print("ENERGY from RANGE INC:", added_energy_cost)
        print("RANGE INC:", range_increase_input+1,"X")
        print("Quicken Value:", quicken)
        #print(tabulate(table, headers=["From","To","Base AP","Base Energy","Cross AP","Cross Energy",
                                       #"Domain","Range","RT","Comment","Chan","AP"], tablefmt="fancy_grid"))
        df = pd.DataFrame(table,columns=["From","To","Base AP","Base Energy","Cross AP","Cross Energy","Domain","Range","RT","Comment","Chan","AP"])
    
    
        printed_output = buffer.getvalue()
        buffer.close()
    
        ax.set_box_aspect([1,1,1])
        ax.view_init(elev=alt, azim=azim)
        lim = max_radius+1
        ax.set_xlim(-lim,lim)
        ax.set_ylim(-lim,lim)
        ax.set_zlim(-lim,lim)
        #plt.show()
        return fig, printed_output, df
    


