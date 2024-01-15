
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.offline as pyo
import io
# Initialize the image buffer only once
buffer = io.BytesIO()

def create_stacked_bar_plot(grouping_column, plot_title, df_cleaned,rot=0, ordering=None):
    # Check if grouping_column is a list, if not, make it a list
    if not isinstance(grouping_column, list):
        grouping_column = [grouping_column]

    # Preparing the data
    acceptance_counts = df_cleaned.groupby(grouping_column + ['Y']).size().unstack().fillna(0)
    total_responses = acceptance_counts.sum(axis=1)
    percentages = acceptance_counts.divide(total_responses, axis=0) * 100

    # Create the stacked bar plot
    plt.figure(figsize=(12, 8))

    # Apply ordering if provided
    if ordering:
        acceptance_counts = acceptance_counts.reindex(ordering)

    # Plotting each segment with actual counts
    for category in acceptance_counts.index:
        total_count = acceptance_counts.loc[category].sum()
        accept_count = acceptance_counts.loc[category, 1]
        reject_count = acceptance_counts.loc[category, 0]

        # Percentages for annotation
        accept_percentage = (accept_count / total_count) * 100
        reject_percentage = (reject_count / total_count) * 100

        plt.bar(category, accept_count, label='Accepted (Y=1)' if category == acceptance_counts.index[0] else "", color='green', alpha=0.6)
        plt.bar(category, reject_count, bottom=accept_count, label='Rejected (Y=0)' if category == acceptance_counts.index[0] else "", color='red', alpha=0.6)

        # Annotating the bars with percentages
        if accept_count > 0:
            plt.text(category, accept_count / 2, f'{accept_percentage:.1f}%', ha='center', va='center', color='black')
        if reject_count > 0:
            plt.text(category, accept_count + reject_count / 2, f'{reject_percentage:.1f}%', ha='center', va='center', color='black')

    plt.xticks(rotation=rot)
    plt.title(plot_title)
    plt.ylabel('Frequency')
    plt.xlabel(' & '.join(grouping_column))
    plt.legend()
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Adjust bottom margin

  
    image_base64 = save_plot_as_base64(buffer, plt)


    return image_base64

# Example usage:
# image_base64 = create_stacked_bar_plot(['coupon', 'income_bracket'], df_cleaned, 45,ordering)



def create_stacked_bar_plot_multi(grouping_columns, plot_title, df_cleaned,rotation=0, yscale='linear',ordering=None):
    # Ensure grouping_columns is a list
    if not isinstance(grouping_columns, list):
        grouping_columns = [grouping_columns]

    # Preparing the data
    acceptance_counts = df_cleaned.groupby(grouping_columns + ['Y']).size().unstack().fillna(0)
    total_responses = acceptance_counts.sum(axis=1)
    percentages = acceptance_counts.divide(total_responses, axis=0) * 100

    # Create the stacked bar plot
    plt.figure(figsize=(12, 8))

    # Apply ordering if provided
    if ordering:
        acceptance_counts = acceptance_counts.reindex(ordering)

    # Plotting each segment with actual counts
    for index, row in acceptance_counts.iterrows():
        category_label = str(index)  # Convert tuple to string for labeling
        total_count = row.sum()
        accept_count = row.get(1, 0)
        reject_count = row.get(0, 0)

        # Percentages for annotation
        accept_percentage = (accept_count / total_count) * 100
        reject_percentage = (reject_count / total_count) * 100

        plt.bar(category_label, accept_count, label='Accepted (Y=1)' if index == acceptance_counts.index[0] else "", color='green', alpha=0.6)
        plt.bar(category_label, reject_count, bottom=accept_count, label='Rejected (Y=0)' if index == acceptance_counts.index[0] else "", color='red', alpha=0.6)

        # Annotating the bars with percentages
        if accept_count > 0:
            plt.text(category_label, accept_count / 2, f'{accept_percentage:.1f}%', ha='center', va='center', color='black')
        if reject_count > 0:
            plt.text(category_label, accept_count + reject_count / 2, f'{reject_percentage:.1f}%', ha='center', va='center', color='black')

    plt.xticks(rotation=rotation)
    plt.title(plot_title)
    plt.ylabel('Frequency')
    plt.xlabel(' & '.join(grouping_columns))
    plt.legend()
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Adjust bottom margin


    image_base64 = save_plot_as_base64(buffer, plt, rotation,yscale)


    return image_base64

# Example usage:
# image_base64 = create_stacked_bar_plot(['Department', 'Experience_Level'], 'Department and Experience Level Acceptance Rate', df_cleaned, ordering=['Sales', 'HR', 'IT'])

def create_subplot_grid(df, columns, plot_title, rotation=0, yscale='linear'):
    # Create a 3x2 subplot grid
    fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharex=False)
    axes = axes.flatten()

    for i, column in enumerate(columns):
        # Group by the column and calculate acceptance counts
        acceptance_counts = df.groupby([column, 'Y']).size().unstack().fillna(0)
        total_responses = acceptance_counts.sum(axis=1)
        percentages = acceptance_counts.divide(total_responses, axis=0) * 100

        # Plotting each segment with actual counts
        for index, row in acceptance_counts.iterrows():
            category_label = str(index)  # Convert tuple to string for labeling
            total_count = row.sum()
            accept_count = row.get(1, 0)
            reject_count = row.get(0, 0)

            # Percentages for annotation
            accept_percentage = (accept_count / total_count) * 100
            reject_percentage = (reject_count / total_count) * 100

            axes[i].bar(category_label, accept_count, color='green', alpha=0.6)
            axes[i].bar(category_label, reject_count, bottom=accept_count, color='red', alpha=0.6)

            # Annotating the bars with percentages
            if accept_count > 0:
                axes[i].text(category_label, accept_count / 2, f'{accept_percentage:.1f}%', ha='center', va='center',
                             color='black')
            if reject_count > 0:
                axes[i].text(category_label, accept_count + reject_count / 2, f'{reject_percentage:.1f}%', ha='center',
                             va='center', color='black')

        axes[i].set_title(f'Stacked Bar Plot for {column}')
        axes[i].set_xlabel(column)
        axes[i].set_ylabel('Frequency')
        axes[i].tick_params(axis='x', rotation=rotation)

    # Adjust layout and add the main title
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, hspace=0.6)  # Increased hspace for better spacing between rows
    fig.suptitle(plot_title, fontsize=16)
    fig.subplots_adjust(wspace=0.4)

    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    image_base64 = save_plot_as_base64(buffer, plt, rotation, yscale)

    return image_base64

def create_overall_stacked_bar_plot(plot_title, df_cleaned, rotation=0, yscale='linear'):
    plt.figure(figsize=(12, 8))

    # Calculate overall acceptance counts
    overall_acceptance = df_cleaned['Y'].value_counts().reindex([0, 1], fill_value=0)
    overall_total = overall_acceptance.sum()
    overall_accept_count = overall_acceptance.get(1, 0)
    overall_reject_count = overall_acceptance.get(0, 0)

    # Overall percentages for annotation
    overall_accept_percentage = (overall_accept_count / overall_total) * 100 if overall_total > 0 else 0
    overall_reject_percentage = (overall_reject_count / overall_total) * 100 if overall_total > 0 else 0

    # Plot overall bars
    plt.bar('Overall', overall_accept_count, color='green', alpha=0.6)
    plt.bar('Overall', overall_reject_count, bottom=overall_accept_count, color='red', alpha=0.6)

    # Annotate overall bars
    if overall_accept_count > 0:
        plt.text('Overall', overall_accept_count / 2, f'{overall_accept_percentage:.1f}%', ha='center', va='center', color='black')
    if overall_reject_count > 0:
        plt.text('Overall', overall_accept_count + overall_reject_count / 2, f'{overall_reject_percentage:.1f}%', ha='center', va='center', color='black')

    # Set plot parameters
    plt.xticks(rotation=rotation)
    plt.title(plot_title)
    plt.ylabel('Frequency')
    plt.xlabel('Overall Data')
    plt.legend(['Accepted (Y=1)', 'Rejected (Y=0)'])
    plt.yscale(yscale)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)
    
    image_base64 = save_plot_as_base64(buffer, plt, rotation,yscale)



    return image_base64
#  Example usage
# plot_title = 'Overall Acceptance Rate'
# image_base64 = create_overall_stacked_bar_plot(plot_title, df_cleaned, rotation=0, yscale='log')


def create_stacked_bar_plot_with_filters(filters, filter_labels, plot_title, group_descriptions, df_cleaned, rotation=0, yscale='linear'):
    plt.figure(figsize=(12, 8))

    # Apply each filter and plot the corresponding bar
    for i, (filter_condition, label) in enumerate(zip(filters, filter_labels)):
        # Apply filter
        filtered_df = df_cleaned[filter_condition]

        # Calculate acceptance counts
        acceptance_counts = filtered_df['Y'].value_counts().reindex([0, 1], fill_value=0)
        total_count = acceptance_counts.sum()
        accept_count = acceptance_counts.get(1, 0)
        reject_count = acceptance_counts.get(0, 0)

        # Percentages for annotation
        accept_percentage = (accept_count / total_count) * 100 if total_count else 0
        reject_percentage = (reject_count / total_count) * 100 if total_count else 0

        # Plot bars
        plt.bar(label, accept_count, color='green', alpha=0.6)
        plt.bar(label, reject_count, bottom=accept_count, color='red', alpha=0.6)

        # Annotate bars
        if accept_count > 0:
            plt.text(label, accept_count / 2, f'{accept_percentage:.1f}%', ha='center', va='center', color='black')
        if reject_count > 0:
            plt.text(label, accept_count + reject_count / 2, f'{reject_percentage:.1f}%', ha='center', va='center', color='black')

    # Set plot parameters
    plt.xticks(rotation=rotation)
    plt.title(plot_title)
    plt.ylabel('Frequency')
    plt.xlabel('Groups')
    plt.yscale(yscale)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)

    # Create custom legend entries
#     legend_entries = [plt.Line2D([0], [0], color='w', marker='o', markerfacecolor='g', label=group_descriptions[label]) for label in filter_labels]
#     plt.legend(handles=legend_entries, title='Group Descriptions')

    legend_labels = [f'{key}: {value}' for key, value in group_descriptions.items()]
    plt.legend(title='Group Descriptions', title_fontsize='13', loc='upper right', labels=legend_labels, borderaxespad=0.)

    image_base64 = save_plot_as_base64(buffer, plt, rotation,yscale)


    return image_base64


# function to save a png to a buffer in memory

def save_plot_as_base64(buffer, plt, rotation_angle=0, yscale='linear'):
    # Reset buffer position before saving a new plot
    buffer.seek(0)

    # Format the plot
    plt.xticks(rotation=rotation_angle)
    plt.yscale(yscale)
    plt.tight_layout()
    # Save the plot to the buffer
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()

    # Reset buffer position and encode the image as base64
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    return image_base64

# Usage example
# Plot something with matplotlib...
# image_base64 = save_plot_as_base64(buffer, plt)
