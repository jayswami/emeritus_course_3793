"""
BarPlotter: A Python module for creating comprehensive bar plots

This module, developed by Jayswami Inc., provides a suite of functions for generating stacked bar plots that juxtapose acceptance and rejection rates against frequency on the Y-axis. This approach presents a complete and nuanced view of data distribution and trends. Utilizing seaborn for its robust plotting capabilities, the module is designed for insightful data analysis and clear visual presentations.

Created by: Jayswami Inc.
GitHub: https://github.com/jayswami
Date: 2024
License: MIT License (Refer to the LICENSE file for more details)

The use of this module is subject to the terms of the MIT License. It is provided with no warranty or guarantee of support. For full license details, please see the LICENSE file distributed with this module.
"""

"""
BarPlotter Module
-----------------

Created by: Jay Swami
GitHub: https://github.com/jayswami
Creation Date: 2024-01-18
Last Updated: 2024-01-18

Note: Documentation for this module is currently a work in progress and will be updated soon.

Module Description:
This module, 'BarPlotter', offers a suite of utility functions specifically tailored for visualizing coupon acceptance 
and rejection data. Utilizing Seaborn, a powerful Python visualization library, it creates stacked bar graphs that 
juxtapose acceptance and rejection rates using percentages, with frequency as the Y-axis.

The core methodology of the module is to provide a comprehensive view of the data. By simultaneously presenting 
acceptance and rejection rates, these visualizations avoid potential misinterpretations that could arise from 
analyzing acceptance rates in isolation. This dual representation ensures a more balanced and insightful analysis, 
reflecting both the volume of offers and the context of rejections.

Key Features:
- Variety of Bar Plot Flavors: The module includes different types of bar plot functions, each designed to represent 
  the data in unique and informative ways. This versatility allows for tailored visualizations suited to specific 
  analytical needs.
- Seaborn Integration: Leveraging Seaborn's advanced plotting capabilities, the module ensures that the visualizations 
  are not only informative but also aesthetically appealing.
- Comprehensive Analysis: By providing tools to visualize data across various dimensions like demographics, time 
  periods, or other categorical variables, 'BarPlotter' facilitates a deeper understanding of coupon acceptance and 
  rejection patterns.

Each function in this module is well-documented, detailing its purpose, inputs, and expected outputs. This 
documentation aims to make the module accessible and easy to use for anyone looking to conduct a detailed analysis 
of coupon data.

Copyright (c) 2024 Jay Swami. All rights reserved.
...


BarPlotter is made available under the MIT License. This license allows for a wide range of uses, giving you the 
freedom to use, modify, and distribute the software as you see fit. For full license terms, please refer to the 
LICENSE file in the repository.

...


"""

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


def create_stacked_bar_plot(grouping_column, plot_title, df_cleaned, rot=0, ordering=None):
    """
        Creates a stacked bar plot to visualize the acceptance and rejection rates.

        This function generates a stacked bar plot that displays the distribution frequency
        of accepted and rejected responses in the given DataFrame. The acceptance and
        rejection rates are annotated on the bars for clarity.

        Parameters:
        - grouping_column (str or list): Column name(s) in the DataFrame to group data by.
                                         If a string is provided, it is converted into a list.
        - plot_title (str): Title of the plot.
        - df_cleaned (DataFrame): The cleaned DataFrame containing the data to be plotted.
        - rot (int, optional): Degrees of rotation for x-axis labels. Default is 0.
        - ordering (list, optional): Specific order for categories on the x-axis. Default is None.

        Returns:
        - str: A base64 string representation of the generated plot.

        The function calculates the acceptance and rejection counts and percentages for each
        category in the grouping column. It then creates a stacked bar plot with these values,
        where the y-axis represents the frequency and the bars are color-coded for acceptance
        (green) and rejection (red). Percentages are displayed on the bars for easy reading.

        """
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

        plt.bar(category, accept_count, label='Accepted (Y=1)' if category == acceptance_counts.index[0] else "",
                color='green', alpha=0.6)
        plt.bar(category, reject_count, bottom=accept_count,
                label='Rejected (Y=0)' if category == acceptance_counts.index[0] else "", color='red', alpha=0.6)

        # Annotating the bars with percentages
        if accept_count > 0:
            plt.text(category, accept_count / 2, f'{accept_percentage:.1f}%', ha='center', va='center', color='black')
        if reject_count > 0:
            plt.text(category, accept_count + reject_count / 2, f'{reject_percentage:.1f}%', ha='center', va='center',
                     color='black')

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


def create_stacked_bar_plot_multi(grouping_columns, plot_title, df_cleaned, rotation=0, yscale='linear', ordering=None):
    """
        Create a stacked bar plot with multiple grouping columns and return the plot as a base64-encoded image string
        along with a DataFrame containing counts and acceptance rates for each category.

        Parameters:
        - grouping_columns (str or list): The column(s) used for grouping the data.
        - plot_title (str): The title for the stacked bar plot.
        - df_cleaned (DataFrame): The cleaned DataFrame containing the data to be plotted.
        - rotation (int, optional): The rotation angle for x-axis labels. Default is 0.
        - yscale (str, optional): The y-axis scale type ('linear' or 'log'). Default is 'linear'.
        - ordering (list, optional): A list specifying the desired order of categories. Default is None.

        Returns:
        - A tuple containing the base64-encoded image string and a DataFrame with counts and acceptance rates.

        """

    # Ensure grouping_columns is a list
    if not isinstance(grouping_columns, list):
        grouping_columns = [grouping_columns]

    # Preparing the data
    acceptance_counts = df_cleaned.groupby(grouping_columns + ['Y']).size().unstack().fillna(0)

    # Calculate total responses and percentages
    total_responses = acceptance_counts.sum(axis=1)
    percentages = acceptance_counts.divide(total_responses, axis=0) * 100

    # Create the stacked bar plot
    plt.figure(figsize=(12, 8))

    # Apply ordering if provided
    if ordering:
        acceptance_counts = acceptance_counts.reindex(ordering)

    # Create a list to accumulate results
    results_list = []

    # Plotting each segment with actual counts
    for index, row in acceptance_counts.iterrows():
        category_label = str(index)  # Convert tuple to string for labeling
        total_count = row.sum()
        accept_count = row.get(1, 0)
        reject_count = row.get(0, 0)

        # Percentages for annotation
        accept_percentage = (accept_count / total_count) * 100
        reject_percentage = (reject_count / total_count) * 100

        # Append results for this category
        results_list.append({
            'category_label': category_label,
            'total_count': total_count,
            'accept_count': accept_count,
            'reject_count': reject_count,
            'accept_percentage': accept_percentage,
            'reject_percentage': reject_percentage
        })

        plt.bar(category_label, accept_count, label='Accepted (Y=1)' if index == acceptance_counts.index[0] else "",
                color='green', alpha=0.6)
        plt.bar(category_label, reject_count, bottom=accept_count,
                label='Rejected (Y=0)' if index == acceptance_counts.index[0] else "", color='red', alpha=0.6)

        # Annotating the bars with percentages
        if accept_count > 0:
            plt.text(category_label, accept_count / 2, f'{accept_percentage:.1f}%', ha='center', va='center',
                     color='black')
        if reject_count > 0:
            plt.text(category_label, accept_count + reject_count / 2, f'{reject_percentage:.1f}%', ha='center',
                     va='center', color='black')

    # Customize plot appearance and labels
    plt.xticks(rotation=rotation)
    plt.title(plot_title)
    plt.ylabel('Frequency')
    plt.xlabel(' & '.join(grouping_columns))
    plt.legend()
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Adjust bottom margin

    image_base64 = save_plot_as_base64(buffer, plt, rotation, yscale)

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results_list)

    return image_base64, results_df


# Example usage:
# image_base64 = create_stacked_bar_plot(['Department', 'Experience_Level'], 'Department and Experience Level Acceptance Rate', df_cleaned, ordering=['Sales', 'HR', 'IT'])
def create_subplot_grid(df, columns, plot_title, rotation=0, yscale='linear'):
    """
    Creates a grid of subplot stacked bar plots for the given DataFrame and columns.

    Parameters:
    - df (DataFrame): The DataFrame containing the data to plot.
    - columns (list): A list of column names in the DataFrame to create subplots for.
    - plot_title (str): The title for the overall figure.
    - rotation (int): The rotation angle for x-axis labels. Default is 0.
    - yscale (str): The y-axis scale type ('linear' or 'log'). Default is 'linear'.

    Returns:
    - A tuple containing the base64 encoded image string and a DataFrame of results.
    """

    # List to collect DataFrame rows for results
    results_list = []

    # Create a 3x2 subplot grid
    fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharex=False)
    axes = axes.flatten()

    # Iterate over each column to create a subplot
    for i, column in enumerate(columns):
        # Group by the specified column and 'Y', calculate counts
        acceptance_counts = df.groupby([column, 'Y']).size().unstack().fillna(0)
        total_responses = acceptance_counts.sum(axis=1)

        # Plotting each category within the column
        for index, row in acceptance_counts.iterrows():
            category_label = str(index)
            total_count = row.sum()
            accept_count = row.get(1, 0)
            reject_count = row.get(0, 0)
            accept_percentage = (accept_count / total_count) * 100
            reject_percentage = (reject_count / total_count) * 100

            # Append results for this category
            results_list.append({
                'subplot_label': f'Stacked Bar Plot for {column}',
                'category': category_label,
                'total_count': total_count,
                'accept_count': accept_count,
                'reject_count': reject_count,
                'accept_percentage': accept_percentage,
                'reject_percentage': reject_percentage
            })

            # Plotting and annotating bars
            axes[i].bar(category_label, accept_count, color='green', alpha=0.6)
            axes[i].bar(category_label, reject_count, bottom=accept_count, color='red', alpha=0.6)
            if accept_count > 0:
                axes[i].text(category_label, accept_count / 2, f'{accept_percentage:.1f}%', ha='center', va='center', color='black')
            if reject_count > 0:
                axes[i].text(category_label, accept_count + reject_count / 2, f'{reject_percentage:.1f}%', ha='center', va='center', color='black')

        # Setting subplot titles and labels
        axes[i].set_title(f'Stacked Bar Plot for {column}')
        axes[i].set_xlabel(column)
        axes[i].set_ylabel('Frequency')
        axes[i].tick_params(axis='x', rotation=rotation)

    # Adjust layout and titles
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, hspace=0.6)
    fig.suptitle(plot_title, fontsize=16)
    fig.subplots_adjust(wspace=0.4)

    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    # Save the plot as a base64 encoded image
    image_base64 = save_plot_as_base64(buffer, plt, rotation, yscale)

    # Convert results list to DataFrame
    results_df = pd.concat([pd.DataFrame([row]) for row in results_list], ignore_index=True)

    return image_base64, results_df



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
        plt.text('Overall', overall_accept_count / 2, f'{overall_accept_percentage:.1f}%', ha='center', va='center',
                 color='black')
    if overall_reject_count > 0:
        plt.text('Overall', overall_accept_count + overall_reject_count / 2, f'{overall_reject_percentage:.1f}%',
                 ha='center', va='center', color='black')

    # Set plot parameters
    plt.xticks(rotation=rotation)
    plt.title(plot_title)
    plt.ylabel('Frequency')
    plt.xlabel('Overall Data')
    plt.legend(['Accepted (Y=1)', 'Rejected (Y=0)'])
    plt.yscale(yscale)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)

    image_base64 = save_plot_as_base64(buffer, plt, rotation, yscale)

    return image_base64


#  Example usage
# plot_title = 'Overall Acceptance Rate'
# image_base64 = create_overall_stacked_bar_plot(plot_title, df_cleaned, rotation=0, yscale='log')

def create_stacked_bar_plot_with_filters(filters, filter_labels, plot_title, group_descriptions, df_cleaned, rotation=0,
                                         yscale='linear'):
    plt.figure(figsize=(12, 8))

    # DataFrame to store results
    results_list = []  # List to collect DataFrame rows

    # DataFrame to store results
    #     results_df = pd.DataFrame(columns=['Group', 'Total_Count', 'Accept_Count', 'Reject_Count', 'Accept_Percentage', 'Reject_Percentage'])

    # Apply each filter and plot the corresponding bar
    for i, (filter_condition, label) in enumerate(zip(filters, filter_labels)):
        # Apply filter
        if filter_condition is not None:
            filtered_df = df_cleaned.query(filter_condition) if isinstance(filter_condition, str) else df_cleaned[
                filter_condition]
        else:
            filtered_df = df_cleaned

        # Calculate acceptance counts
        acceptance_counts = filtered_df['Y'].value_counts().reindex([0, 1], fill_value=0)
        total_count = acceptance_counts.sum()
        accept_count = acceptance_counts.get(1, 0)
        reject_count = acceptance_counts.get(0, 0)

        # Percentages for annotation
        accept_percentage = (accept_count / total_count) * 100 if total_count else 0
        reject_percentage = (reject_count / total_count) * 100 if total_count else 0

        # Add row to results list
        results_list.append({
            'group_label': label,
            'total_count': total_count,
            'accept_count': accept_count,
            'reject_count': reject_count,
            'accept_percentage': accept_percentage,
            'reject_percentage': reject_percentage
        })

        # Add results to DataFrame
        #         results_df = results_df.append({'Group': label, 'Total_Count': total_count, 'Accept_Count': accept_count,
        #                                         'Reject_Count': reject_count, 'Accept_Percentage': accept_percentage,
        #                                         'Reject_Percentage': reject_percentage}, ignore_index=True)

        # Plot bars
        plt.bar(label, accept_count, color='green', alpha=0.6)
        plt.bar(label, reject_count, bottom=accept_count, color='red', alpha=0.6)

        # Annotate bars
        if accept_count > 0:
            plt.text(label, accept_count / 2, f'{accept_percentage:.1f}%', ha='center', va='center', color='black')
        if reject_count > 0:
            plt.text(label, accept_count + reject_count / 2, f'{reject_percentage:.1f}%', ha='center', va='center',
                     color='black')

    # Set plot parameters
    plt.xticks(rotation=rotation)
    plt.title(plot_title)
    plt.ylabel('Frequency')
    plt.xlabel('Groups')
    plt.yscale(yscale)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)

    if group_descriptions is not None:
        legend_labels = [f'{key}: {value}' for key, value in group_descriptions.items()]
        plt.legend(title='Group Descriptions', title_fontsize='13', loc='upper right', labels=legend_labels,
                   borderaxespad=0.)

    image_base64 = save_plot_as_base64(buffer, plt, rotation, yscale)

    results_df = pd.concat([pd.DataFrame([row]) for row in results_list], ignore_index=True)

    return image_base64, results_df


# def create_stacked_bar_plot_with_filters(filters, filter_labels, plot_title, group_descriptions, df_cleaned, rotation=0, yscale='linear'):
#     plt.figure(figsize=(12, 8))
#
#     # Apply each filter and plot the corresponding bar
#     for i, (filter_condition, label) in enumerate(zip(filters, filter_labels)):
#         # Apply filter
#         if filter_condition is not None:
#             filtered_df = df_cleaned.query(filter_condition) if isinstance(filter_condition, str) else df_cleaned[
#                 filter_condition]
#         else:
#             filtered_df = df_cleaned
#
#
#         # Calculate acceptance counts
#         acceptance_counts = filtered_df['Y'].value_counts().reindex([0, 1], fill_value=0)
#         total_count = acceptance_counts.sum()
#         accept_count = acceptance_counts.get(1, 0)
#         reject_count = acceptance_counts.get(0, 0)
#
#         # Percentages for annotation
#         accept_percentage = (accept_count / total_count) * 100 if total_count else 0
#         reject_percentage = (reject_count / total_count) * 100 if total_count else 0
#
#         # Plot bars
#         plt.bar(label, accept_count, color='green', alpha=0.6)
#         plt.bar(label, reject_count, bottom=accept_count, color='red', alpha=0.6)
#
#         # Annotate bars
#         if accept_count > 0:
#             plt.text(label, accept_count / 2, f'{accept_percentage:.1f}%', ha='center', va='center', color='black')
#         if reject_count > 0:
#             plt.text(label, accept_count + reject_count / 2, f'{reject_percentage:.1f}%', ha='center', va='center', color='black')
#
#     # Set plot parameters
#     plt.xticks(rotation=rotation)
#     plt.title(plot_title)
#     plt.ylabel('Frequency')
#     plt.xlabel('Groups')
#     plt.yscale(yscale)
#     plt.tight_layout()
#     plt.subplots_adjust(bottom=0.2)
#
#
#     if group_descriptions is not None:
#         legend_labels = [f'{key}: {value}' for key, value in group_descriptions.items()]
#         plt.legend(title='Group Descriptions', title_fontsize='13', loc='upper right', labels=legend_labels,
#                    borderaxespad=0.)
#
#     image_base64 = save_plot_as_base64(buffer, plt, rotation,yscale)
#
#
#     return image_base64


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


def create_subplot_grid_dflist(dfs, column, plot_title, subplot_labels, rotation=0, yscale='linear', ordering=None,
                               buffer=io.BytesIO()):
    # DataFrame to store results
    results_list = []  # List to collect DataFrame rows

    # Check if the number of DataFrames matches the number of subplot labels
    if len(dfs) != len(subplot_labels):
        raise ValueError("The number of DataFrames and subplot labels must be the same")

    # Create a 2x2 subplot grid
    fig, axes = plt.subplots(2, 2, figsize=(15, 10), sharex=False)
    axes = axes.flatten()

    for i, df in enumerate(dfs):
        # Group by the column and calculate acceptance counts
        acceptance_counts = df.groupby([column, 'Y']).size().unstack().fillna(0)
        total_responses = acceptance_counts.sum(axis=1)

        if ordering:
            acceptance_counts = acceptance_counts.reindex(ordering)

        # Plotting each segment with actual counts
        for index, row in acceptance_counts.iterrows():
            category_label = str(index)
            total_count = row.sum()
            accept_count = row.get(1, 0)
            reject_count = row.get(0, 0)
            accept_percentage = (accept_count / total_count) * 100
            reject_percentage = (reject_count / total_count) * 100

            # Add row to results list
            results_list.append({
                'subplot_label': subplot_labels[i],
                'category': category_label,
                'total_count': total_count,
                'accept_count': accept_count,
                'reject_count': reject_count,
                'accept_percentage': accept_percentage,
                'reject_percentage': reject_percentage
            })

            # Plotting
            axes[i].bar(category_label, accept_count, color='green', alpha=0.6)
            axes[i].bar(category_label, reject_count, bottom=accept_count, color='red', alpha=0.6)

            # Annotating the bars with percentages
            if accept_count > 0:
                axes[i].text(category_label, accept_count / 2, f'{accept_percentage:.1f}%', ha='center', va='center',
                             color='black')
            if reject_count > 0:
                axes[i].text(category_label, accept_count + reject_count / 2, f'{reject_percentage:.1f}%', ha='center',
                             va='center', color='black')

        axes[i].set_title(subplot_labels[i])
        axes[i].set_xlabel(column)
        axes[i].set_ylabel('Frequency')
        axes[i].tick_params(axis='x', rotation=rotation)
        axes[i].set_yscale(yscale)

    # Adjust layout and add the main title
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, hspace=0.6)
    fig.suptitle(plot_title, fontsize=16)
    fig.subplots_adjust(wspace=0.4)

    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    # Save the plot as a base64 encoded image using the provided function
    image_base64 = save_plot_as_base64(buffer, plt, rotation, yscale)

    # Convert results list to DataFrame
    results_df = pd.concat([pd.DataFrame([row]) for row in results_list], ignore_index=True)

    return image_base64, results_df



