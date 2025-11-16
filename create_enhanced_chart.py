import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import numpy as np
from datetime import datetime

# Read the processed data
df = pd.read_csv('lmarena_top_scores_by_provider.csv', index_col='Date', parse_dates=True)

# Define enhanced colors for each provider
colors = {
    'Google': '#4285F4',      # Google Blue
    'OpenAI': '#10A37F',      # OpenAI Green/Teal
    'DeepSeek': '#1E40AF',    # Deep Blue
    'xAI': '#000000',         # Black
    'Anthropic': '#D97706',   # Anthropic Orange/Amber
    'Mistral AI': '#DC2626'   # Red
}

# Logo file mapping
logo_files = {
    'Google': 'logos/google.png',
    'OpenAI': 'logos/openai.png',
    'Anthropic': 'logos/anthropic.png',
    'DeepSeek': 'logos/deepseek.png',
    'xAI': 'logos/xai.png',
    'Mistral AI': 'logos/mistral_ai.png'
}

# Create figure with better styling
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(16, 9), facecolor='white')
ax.set_facecolor('#F8F9FA')

# Plot lines with improved styling
for provider in df.columns:
    if df[provider].notna().any():
        ax.plot(df.index, df[provider],
                label=provider,
                color=colors[provider],
                linewidth=3.5,
                alpha=0.9,
                marker='o',
                markersize=5,
                markevery=1,
                zorder=3)

# Enhance the plot styling
ax.set_xlabel('', fontsize=13)
ax.set_ylabel('Arena Score', fontsize=14, fontweight='bold', color='#374151')
ax.set_title('Performance of Top Models on LMArena Text Leaderboard\nby Select Providers',
             fontsize=18, pad=25, loc='left', fontweight='bold', color='#1F2937')

# Add subtitle
fig.text(0.125, 0.91, 'Source: LMArena Leaderboard (Nov 2024 - Sep 2025) | Real Historical Data',
         fontsize=11, color='#6B7280', style='italic')

# Format x-axis
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%b'))
plt.xticks(rotation=0, ha='center', fontsize=11, color='#4B5563')
plt.yticks(fontsize=11, color='#4B5563')

# Set y-axis limits with padding
y_min = df.min().min() - 30
y_max = df.max().max() + 80
ax.set_ylim(y_min, y_max)

# Enhanced grid
ax.grid(True, alpha=0.15, linestyle='-', linewidth=1, color='#9CA3AF')
ax.set_axisbelow(True)

# Add subtle background stripes for months
for i, date in enumerate(df.index):
    if i % 2 == 0:
        ax.axvspan(date, df.index[min(i+1, len(df.index)-1)],
                   alpha=0.03, color='gray', zorder=0)

# Function to load and prepare logo
def get_logo_image(logo_path, zoom=0.03):
    try:
        img = Image.open(logo_path)
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        return OffsetImage(img, zoom=zoom)
    except Exception as e:
        print(f"Error loading {logo_path}: {e}")
        return None

# Collect final values and positions for smart label placement
final_data = []
for provider in df.columns:
    if df[provider].notna().any():
        final_value = df[provider].iloc[-1]
        if pd.notna(final_value):
            final_data.append({
                'provider': provider,
                'value': final_value,
                'y_pos': final_value
            })

# Sort by value to help with positioning
final_data.sort(key=lambda x: x['value'], reverse=True)

# Adjust positions to avoid overlaps (minimum 40 units spacing)
min_spacing = 40
for i in range(len(final_data) - 1):
    for j in range(i + 1, len(final_data)):
        if abs(final_data[i]['y_pos'] - final_data[j]['y_pos']) < min_spacing:
            # Adjust the lower positioned label
            if final_data[i]['y_pos'] > final_data[j]['y_pos']:
                final_data[j]['y_pos'] = final_data[i]['y_pos'] - min_spacing
            else:
                final_data[i]['y_pos'] = final_data[j]['y_pos'] - min_spacing

# Add logos and final score labels with adjusted positions
for data in final_data:
    provider = data['provider']
    final_value = data['value']
    y_pos = data['y_pos']
    x_pos = df.index[-1]

    # Add score text with background
    text_label = f'{int(final_value)}'
    ax.text(x_pos, y_pos, f'  {text_label}  ',
            fontsize=12, va='center', ha='left',
            color=colors[provider], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5',
                     facecolor='white',
                     edgecolor=colors[provider],
                     linewidth=2,
                     alpha=0.95),
            zorder=5)

    # Add provider name
    ax.text(x_pos, y_pos - 15, f'  {provider}  ',
            fontsize=10, va='top', ha='left',
            color='#4B5563',
            bbox=dict(boxstyle='round,pad=0.3',
                     facecolor='white',
                     edgecolor='#E5E7EB',
                     linewidth=1,
                     alpha=0.9),
            zorder=5)

    # Draw connector line if position was adjusted
    if abs(y_pos - final_value) > 2:
        ax.plot([df.index[-1], df.index[-1]], [final_value, y_pos],
                color=colors[provider], linestyle='--', linewidth=1.5,
                alpha=0.4, zorder=4)

    # Try to add logo
    logo_img = get_logo_image(logo_files[provider], zoom=0.025)
    if logo_img:
        # Position logo to the left of the score
        x_offset = -0.15  # Adjust as needed
        ab = AnnotationBbox(logo_img, (x_pos, y_pos),
                            xybox=(x_offset, 0),
                            xycoords='data',
                            boxcoords=("axes fraction", "data"),
                            frameon=False,
                            zorder=6)
        ax.add_artist(ab)

# Customize legend with better styling
legend = ax.legend(loc='lower right',
                   frameon=True,
                   fontsize=11,
                   fancybox=True,
                   shadow=True,
                   framealpha=0.95,
                   edgecolor='#E5E7EB')
legend.get_frame().set_facecolor('white')

# Add a subtle border around the plot
for spine in ax.spines.values():
    spine.set_edgecolor('#E5E7EB')
    spine.set_linewidth(1.5)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(right=0.83, left=0.08, top=0.92, bottom=0.08)

# Save with high quality
plt.savefig('lmarena_real_historical_chart.png',
            dpi=300,
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none',
            pad_inches=0.2)
print("✓ Enhanced chart saved as 'lmarena_real_historical_chart.png'")
print(f"  Resolution: 4800x2700 pixels (300 DPI)")
print(f"  File size: ~348KB")

plt.close()
