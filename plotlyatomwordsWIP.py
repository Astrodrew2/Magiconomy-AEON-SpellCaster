import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from tabulate import tabulate
import io
import sys
from contextlib import redirect_stdout
import pandas as pd

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
    "beam": "●",
    "radial": "●—",
    "cone": "<"
}

# ---------------- Helper functions ----------------
def bezier_curve_3d(p0, p1, p2, n_points=50):
    t = np.linspace(0,1,n_points)
    curve = ((1-t)**2)[:,None]*p0 + (2*((1-t)*t))[:,None]*p1 + (t**2)[:,None]*p2
    return curve[:,0], curve[:,1], curve[:,2]

import numpy as np
import plotly.graph_objects as go

def draw_electron_connection_plotly(fig, p1, p2, n_lines=1, spacing=0.15, sec1=None, sec2=None,
                                    arch_factor=0.3, flip=True, quicken=0, chann=2, chann2=1, 
                                    tick_len=0.5, vig=2, fiver=2):
    p1 = np.array(p1)
    p2 = np.array(p2)
    distance = np.linalg.norm(p2 - p1)
    arch_height = distance * arch_factor
    offsets = [0] if n_lines == 1 else np.linspace(-(n_lines-1)/2*spacing, (n_lines-1)/2*spacing, n_lines)
    lines_drawn = 0
    used_quicken = 0
    cross_sector_extra = 0
    tick_count = chann2 if chann==1 else 0
    tick_count = min(tick_count, n_lines)

    for i, off in enumerate(offsets):
        is_red = quicken > used_quicken
        used_quicken += int(is_red)

        if sec1 == sec2:
            # Straight line
            vec = p2 - p1
            if np.linalg.norm(vec[:2]) == 0:
                perp = np.array([1,0,0])
            else:
                perp = np.array([-vec[1], vec[0], 0])
            perp = perp / np.linalg.norm(perp) * off
            x_line = [p1[0]+perp[0], p2[0]+perp[0]]
            y_line = [p1[1]+perp[1], p2[1]+perp[1]]
            z_line = [p1[2]+perp[2], p2[2]+perp[2]]

            fig.add_trace(go.Scatter3d(
                x=x_line, y=y_line, z=z_line,
                mode='lines',
                line=dict(color='black', width=2 if not is_red else 3, dash='dash' if is_red else 'solid'),
                showlegend=False
            ))

            # Ticks
            if i < tick_count:
                mid = (p1 + p2)/2 + perp
                tangent = vec / np.linalg.norm(vec)
                perp3 = np.cross(tangent, np.array([0,0,1.0]))
                if np.linalg.norm(perp3)<1e-6:
                    perp3 = np.cross(tangent, np.array([0,1,0]))
                perp3 /= np.linalg.norm(perp3)
                tick1 = mid + perp3*(tick_len/2)
                tick2 = mid - perp3*(tick_len/2)
                fig.add_trace(go.Scatter3d(
                    x=[tick1[0], tick2[0]], y=[tick1[1], tick2[1]], z=[tick1[2], tick2[2]],
                    mode='lines',
                    line=dict(color='black', width=2),
                    showlegend=False
                ))

        else:
            # Curved line (Bezier)
            dir_xy = p2[:2] - p1[:2]
            perp_xy = np.array([-dir_xy[1], dir_xy[0]])
            if flip:
                perp_xy = -perp_xy
            if np.linalg.norm(perp_xy) != 0:
                perp_xy = perp_xy / np.linalg.norm(perp_xy)
            cp = (p1 + p2)/2 + np.append(perp_xy * arch_height + perp_xy*off, 0)
            x_curve, y_curve, z_curve = bezier_curve_3d(p1, cp, p2)
            fig.add_trace(go.Scatter3d(
                x=x_curve, y=y_curve, z=z_curve,
                mode='lines',
                line=dict(color='black', width=2, dash='dash' if is_red else 'solid'),
                showlegend=False
            ))

            # Optional V markers for vig
            if vig == 1 or fiver == 1:
                # Place near start or end of curve
                for idx_frac, size in [(0.1, 0.8 if vig==1 else 0), (0.85, 0.8 if fiver==1 else 0)]:
                    if size == 0:
                        continue
                    idx = max(1, int(len(x_curve)*idx_frac))
                    if idx >= len(x_curve)-1:
                        idx = len(x_curve)//2
                    V_pos = np.array([x_curve[idx], y_curve[idx], z_curve[idx]])
                    tangent = np.array([x_curve[idx+1]-x_curve[idx-1],
                                        y_curve[idx+1]-y_curve[idx-1],
                                        z_curve[idx+1]-z_curve[idx-1]])
                    tangent /= np.linalg.norm(tangent)
                    perp = np.cross(tangent, np.array([0,0,1]))
                    if np.linalg.norm(perp)<1e-6:
                        perp = np.cross(tangent, np.array([0,1,0]))
                    perp /= np.linalg.norm(perp)
                    angle = np.radians(30)
                    leg1 = tangent*np.cos(angle) + perp*np.sin(angle)
                    leg2 = tangent*np.cos(angle) - perp*np.sin(angle)
                    leg1 *= size
                    leg2 *= size
                    fig.add_trace(go.Scatter3d(
                        x=[V_pos[0], V_pos[0]+leg1[0]],
                        y=[V_pos[1], V_pos[1]+leg1[1]],
                        z=[V_pos[2], V_pos[2]+leg1[2]],
                        mode='lines', line=dict(color='black', width=2), showlegend=False
                    ))
                    fig.add_trace(go.Scatter3d(
                        x=[V_pos[0], V_pos[0]+leg2[0]],
                        y=[V_pos[1], V_pos[1]+leg2[1]],
                        z=[V_pos[2], V_pos[2]+leg2[2]],
                        mode='lines', line=dict(color='black', width=2), showlegend=False
                    ))

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
    if base_range_ft < 20:
        return range_increase * 1
    elif 20 <= base_range_ft <= 30:
        return range_increase * 2
    elif 30 < base_range_ft < 100:
        return range_increase * 3
    else:
        return range_increase * 5

import numpy as np
import plotly.graph_objects as go

def draw_modifier_shape_plotly(fig, shape, center, size=1.0, color='black'):
    x0, y0, z0 = center
    z = z0 + 0.5  # lift shape above electron marker

    if shape == "square":
        half = size / 1
        corners = np.array([
            [x0 - half, y0 - half, z],
            [x0 + half, y0 - half, z],
            [x0 + half, y0 + half, z],
            [x0 - half, y0 + half, z],
            [x0 - half, y0 - half, z]  # close the square
        ])
        fig.add_trace(go.Scatter3d(
            x=corners[:, 0], y=corners[:, 1], z=corners[:, 2],
            mode='lines',
            line=dict(color=color, width=2.5),
            showlegend=False
        ))

    elif shape == "double_square":
        half = size / 1
        half2 = half / 1.5
        corners = np.array([
            [x0 - half, y0 - half, z],
            [x0 + half, y0 - half, z],
            [x0 + half, y0 + half, z],
            [x0 - half, y0 + half, z],
            [x0 - half, y0 - half, z]
        ])
        corners2 = np.array([
            [x0 - half2, y0 - half2, z],
            [x0 + half2, y0 - half2, z],
            [x0 + half2, y0 + half2, z],
            [x0 - half2, y0 + half2, z],
            [x0 - half2, y0 - half2, z]
        ])
        for c in [corners, corners2]:
            fig.add_trace(go.Scatter3d(
                x=c[:,0], y=c[:,1], z=c[:,2],
                mode='lines',
                line=dict(color=color, width=1.5),
                showlegend=False
            ))

    elif shape == "circle":
        theta = np.linspace(0, 2 * np.pi, 50)
        xs = x0 + size * np.cos(theta)
        ys = y0 + size * np.sin(theta)
        zs = np.ones_like(xs) * z
        fig.add_trace(go.Scatter3d(
            x=xs, y=ys, z=zs,
            mode='lines',
            line=dict(color=color, width=1.5),
            showlegend=False
        ))

    elif shape == "diamond":
        half = size / 1.5
        corners = np.array([
            [x0, y0 + half, z],                  # top
            [x0 + (0.75*half), y0, z],          # right
            [x0, y0 - half, z],                  # bottom
            [x0 - (0.75*half), y0, z],          # left
            [x0, y0 + half, z]                   # close
        ])
        fig.add_trace(go.Scatter3d(
            x=corners[:, 0], y=corners[:, 1], z=corners[:, 2],
            mode='lines',
            line=dict(color=color, width=1.5),
            showlegend=False
        ))

# ---------------- Main function ----------------
def draw_atom_words_from_dict(words_list, words_dict, modifiers_dict=None, modifiers_to_apply=None,
                              sector_labels=None, tilt=False, alt=90, azim=90, quicken=0, 
                              range_increase_input=0, range_type_change=0):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        if sector_labels is None:
            sector_labels = {1:"↙️",2:"⬇️",3:"↘️",4:"↗️",5:"⬆️",6:"↖️"}

        allowed_sectors = sorted({words_dict[word]["section"] for word in words_list})
        fig = go.Figure()
        
        # Scene setup
        fig.update_layout(scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor="tan",
            aspectmode='cube'),
            width=800, height=800,
            margin=dict(r=10,l=10,b=10,t=10)
        )

        sector_angle = np.pi / 3
        theta_full = np.linspace(0, 2*np.pi, 500)
        all_ranges = []

        # Nucleus
        first_word = words_list[0]
        first_sec = words_dict[first_word]["section"]
        nucleus_label = sector_labels.get(first_sec, str(first_sec))
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers+text',
            marker=dict(symbol='diamond', size=30, color='tan', line=dict(color='black', width=2)),
            text=[nucleus_label],
            textposition='top center',
            textfont=dict(color='black', size=20, family='Arial')
        ))

        # Radius setup
        max_level = max([words_dict[word]["level"] for word in words_list])
        radius_step = 4
        max_radius = max_level * radius_step
        label_radius = max_radius + 0.7

        # Radial lines + sector labels
        for i in range(6):
            angle = i * sector_angle
            x = [0, max_radius * np.cos(angle)]
            y = [0, max_radius * np.sin(angle)]
            z = [0, 0]
            fig.add_trace(go.Scatter3d(
                x=x, y=y, z=z,
                mode='lines',
                line=dict(color='black', width=2, dash='dash'),
                opacity=0.5,
                showlegend=False
            ))

            label_angle = angle + sector_angle / 2
            lx = label_radius * np.cos(label_angle)
            ly = label_radius * np.sin(label_angle)
            lz = 20
            fig.add_trace(go.Scatter3d(
                x=[lx], y=[ly], z=[lz],
                mode='text',
                text=[sector_labels.get(i+1, str(i+1))],
                textposition='middle center',
                textfont=dict(color='black', size=20),
                showlegend=False
            ))

        # Shade allowed sectors
        for sec in allowed_sectors:
            start_angle = (sec - 1) * sector_angle
            end_angle = sec * sector_angle
            theta = np.linspace(start_angle, end_angle, 50)
            r = max_radius + 0.5
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = np.zeros_like(x)
            fig.add_trace(go.Mesh3d(
                x=np.append(0, x),
                y=np.append(0, y),
                z=np.append(0, z),
                color='teal',
                opacity=0.12,
                alphahull=0,
                flatshading=True,
                showscale=False
            ))

        # Draw orbitals
        for L in range(1, max_level + 1):
            r = L * radius_step
            tilt_angle = L * 12 * np.pi / 180 if tilt else 0
            x = r * np.cos(theta_full)
            y = r * np.sin(theta_full) * np.cos(tilt_angle)
            z = r * np.sin(theta_full) * np.sin(tilt_angle)
            fig.add_trace(go.Scatter3d(
                x=x, y=y, z=z,
                mode='lines',
                line=dict(color='black', width=2),
                opacity=0.15,
                showlegend=False
            ))

        # Electron positions
        electron_positions = {}
        rtcEnergy = 0

        # Group words by (level, section)
        grouped = {}
        for word in words_list:
            info = words_dict[word]
            key = (info["level"], info["section"])
            grouped.setdefault(key, []).append((word, info))

        # Draw electrons and mini-orbitals
        for (level, sec), words_in_group in grouped.items():
            r = level * radius_step
            tilt_angle = level * 12 * np.pi / 180 if tilt else 0
            n = len(words_in_group)
            sec_start = (sec - 1) * sector_angle
            sec_center = sec_start + sector_angle / 2
            angles = [sec_center] if n == 1 else np.linspace(sec_center - 0.45, sec_center + 0.45, n)

            for (word, info), angle in zip(words_in_group, angles):
                xe = r * np.cos(angle)
                ye = r * np.sin(angle) * np.cos(tilt_angle)
                ze = r * np.sin(angle) * np.sin(tilt_angle)

                # Electron marker
                fig.add_trace(go.Scatter3d(
                    x=[xe], y=[ye], z=[ze],
                    mode='markers+text',
                    marker=dict(size=12, color='tan', line=dict(color='black', width=2)),
                    text=[word],
                    textposition="top center",
                    textfont=dict(size=10, color='black'),
                    showlegend=False
                ))

                # Range + RT symbols
                rng_num = info.get("range", 0) * (range_increase_input + 1) if not word.endswith(" EN") else info.get("range",0)
                rt_num = info.get("rt",0) + range_type_change
                rng_def = range_dict.get(rng_num)
                rt_def = rt_dict.get(rt_num)
                rng_symbol = range_rt_symbol_dict.get(rng_def, "")
                rt_symbol = range_rt_symbol_dict.get(rt_def, "")

                fig.add_trace(go.Scatter3d(
                    x=[xe], y=[ye-0.1], z=[ze+0.5],
                    mode='text', text=[rng_symbol],
                    textposition="bottom center",
                    textfont=dict(size=9, color='black'),
                    showlegend=False
                ))
                fig.add_trace(go.Scatter3d(
                    x=[xe], y=[ye+0.2], z=[ze-0.5],
                    mode='text', text=[rt_symbol],
                    textposition="top center",
                    textfont=dict(size=5, color='black'),
                    showlegend=False
                ))

                # Store electron positions
                electron_positions[word] = {
                    'pos': (xe, ye, ze),
                    'sector': sec,
                    'level': level,
                    'chann': info.get("chann",2),
                    'chann2': info.get("2chann",1),
                    'info': info.copy()
                }
                if not word.endswith(" EN"):
                    all_ranges.append(rng_def)

        # ---------------- Apply Modifiers ----------------
        modAP = 0
        modEnergy = 0
        if modifiers_dict and modifiers_to_apply:
            for mod_key in modifiers_to_apply:
                mod = modifiers_dict.get(mod_key)
                if not mod: 
                    continue
                for target_word in mod.get("appto", []):
                    if target_word not in electron_positions: 
                        continue
                    pos = electron_positions[target_word]['pos']
                    draw_modifier_shape_plotly(fig, mod.get("shape","square"), pos, size=mod.get("size",2.0))
                    modAP += mod.get("AP",0)
                    modEnergy += mod.get("energy",0)
                    electron_positions[target_word]['info']['AP'] += mod.get("AP",0)
                    electron_positions[target_word]['info']['level'] += mod.get("energy",0)

        # ---------------- Range Increase Mini-Orbitals ----------------
        if range_increase_input > 0:
            base_range_ft = parse_range_value(words_dict[first_word].get("range","self"))
            added_energy_cost = calculate_range_increase_charge(base_range_ft, range_increase_input)
            r_first = electron_positions[first_word]['level'] * radius_step
            for i in range(added_energy_cost):
                r = r_first - (i+1)*0.3
                tilt_angle = 0
                x = r * np.cos(theta_full)
                y = r * np.sin(theta_full) * np.cos(tilt_angle)
                z = r * np.sin(theta_full) * np.sin(tilt_angle)
                fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color='black', width=2), opacity=0.2, showlegend=False))
        else:
            added_energy_cost = 0

        # ---------------- AP & Energy Table ----------------
        table = []
        total_base_AP = total_cross_AP = total_base_energy = total_cross_energy = 0
        remaining_quicken = quicken

        for word in words_list:
            e = electron_positions[word]
            base_AP = e['info'].get("AP",1)
            cross_AP = 0
            base_energy = e['level']
            cross_energy = 0
            total_base_AP += base_AP
            total_base_energy += base_energy
            table.append([
                word, base_AP, base_energy, cross_AP, cross_energy,
                sector_labels.get(e.get("sector","N/A"), str(e['info'].get("sector","N/A"))),
                range_dict.get(e['info'].get("range","N/A"), str(e['info'].get("range","N/A"))),
                rt_dict.get(e['info'].get("rt","N/A"), str(e['info'].get("rt","N/A"))),
                e['info'].get("comment","")
            ])

        total_AP = total_base_AP + total_cross_AP
        total_energy = total_base_energy + total_cross_energy + rtcEnergy

        print("TOTAL AP:", total_AP)
        print("TOTAL ENERGY:", total_energy)
        print("AP from Mods:", modAP)
        print("ENERGY from Mods:", modEnergy + rtcEnergy)
        print("ENERGY from RANGE INC:", added_energy_cost)
        print("RANGE INC:", range_increase_input+1,"X")
        print("Quicken Value:", quicken)

        printed_output = buffer.getvalue()
        buffer.close()
        return fig, printed_output, electron_positions, table


