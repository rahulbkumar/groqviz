import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import glob
import os

# Define the major AI providers we're tracking
providers = {
    'Google': ['Google'],
    'OpenAI': ['OpenAI'],
    'Anthropic': ['Anthropic'],
    'DeepSeek': ['DeepSeek'],
    'xAI': ['xAI'],
    'Mistral AI': ['Mistral AI', 'Mistral']
}

# Month mapping
months = {
    '2024.11': '2024-11-01',
    '2024.12': '2024-12-01',
    '2025.01': '2025-01-01',
    '2025.02': '2025-02-01',
    '2025.03': '2025-03-01',
    '2025.04': '2025-04-01',
    '2025.05': '2025-05-01',
    '2025.06': '2025-06-01',
    '2025.07': '2025-07-01',
    '2025.08': '2025-08-01',
    '2025.09': '2025-09-01',
}

# Data structure to store results
results = {provider: [] for provider in providers.keys()}
dates = []

# Process each monthly file
for month_key in sorted(months.keys()):
    filename = f'monthly_{month_key}.csv'

    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        continue

    print(f"Processing {filename}...")

    try:
        df = pd.read_csv(filename)

        # For each provider, find the highest scoring model
        for provider_name, provider_orgs in providers.items():
            # Filter for this provider's models
            provider_models = df[df['organization'].isin(provider_orgs)]

            if len(provider_models) > 0:
                # Get the highest arena score for this provider
                max_score = provider_models['arena_score'].max()
                results[provider_name].append(max_score)
                print(f"  {provider_name}: {max_score}")
            else:
                # If no models found, use None or previous value
                if len(results[provider_name]) > 0:
                    results[provider_name].append(results[provider_name][-1])
                else:
                    results[provider_name].append(None)
                print(f"  {provider_name}: No data")

        dates.append(pd.to_datetime(months[month_key]))

    except Exception as e:
        print(f"Error processing {filename}: {e}")

# Create DataFrame with results
df_results = pd.DataFrame(results, index=dates)
df_results.index.name = 'Date'

# Save to CSV
df_results.to_csv('lmarena_top_scores_by_provider.csv')
print("\nSaved top scores to 'lmarena_top_scores_by_provider.csv'")

# Create the visualization
fig, ax = plt.subplots(figsize=(14, 8))

# Define colors for each provider (ordered by period)
colors = {
    'Google': '#f43e01',      # Period 1 - Dark red-orange
    'OpenAI': '#fe9e20',      # Period 2 - Orange
    'DeepSeek': '#ffd1a3',    # Period 3 - Light peach
    'xAI': '#69695d',         # Period 4 - Dark gray
    'Anthropic': '#cecebf',   # Period 5 - Light gray
    'Mistral AI': '#f3f3ee'   # Period 6 - Very light beige
}

# Plot lines for each provider
for provider in providers.keys():
    if df_results[provider].notna().any():
        ax.plot(df_results.index, df_results[provider], label=provider,
                color=colors[provider], linewidth=2.5, alpha=0.85)

# Customize the plot
ax.set_xlabel('', fontsize=12)
ax.set_ylabel('Score', fontsize=12)
ax.set_title('Performance of top models on LMArena Text Leaderboard by select providers\nSource: LMArena Leaderboard (2025) | Chart: Real Historical Data',
             fontsize=14, pad=20, loc='left')

# Format x-axis to show month-year
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%b'))
plt.xticks(rotation=0, ha='center')

# Set y-axis limits with some padding
y_min = df_results.min().min() - 50
y_max = df_results.max().max() + 50
ax.set_ylim(y_min, y_max)

# Add grid
ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)

# Add final score labels on the right side
for provider in providers.keys():
    if df_results[provider].notna().any():
        final_value = df_results[provider].iloc[-1]
        if pd.notna(final_value):
            ax.text(df_results.index[-1], final_value, f'{int(final_value)}, {provider}',
                    fontsize=10, va='center', ha='left',
                    color=colors[provider], fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                             edgecolor='none', alpha=0.7))

# Adjust legend
ax.legend(loc='lower right', frameon=True, fontsize=10)

# Adjust layout to prevent label cutoff
plt.tight_layout()
plt.subplots_adjust(right=0.85)

# Save the plot
plt.savefig('lmarena_real_historical_chart.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Chart saved as 'lmarena_real_historical_chart.png'")

# Print summary
print("\n=== Final Scores (September 2025) ===")
for provider in providers.keys():
    if df_results[provider].notna().any():
        final_score = df_results[provider].iloc[-1]
        if pd.notna(final_score):
            print(f"  {provider}: {int(final_score)}")
        else:
            print(f"  {provider}: No data")
