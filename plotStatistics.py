import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import pearsonr
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import warnings
warnings.filterwarnings('ignore')
 
# Read data files
dg = pd.read_excel(r"C:\Users\magnuswe\OneDrive - SINTEF\Dokumenter\Parametere_table_for_plotting_statistics.xlsx")
df = pd.read_csv(r"C:\Users\magnuswe\OneDrive - SINTEF\Dokumenter\parameter_correlations_without_iliac_an.csv", sep=";")
 
# Calculate Bonferroni threshold
bonf_thresh = 1 - 0.95**(1/136)
 
# Variables included in the 6 "strictly significant" correlations (Bonferroni correction)
selected_vars = ["MaxWSSaorta(dynes(cm^2)", "meanTAWSSaneurysm", "Tortuosity", "VFT",
                "Dmax_hyd (cm)", "meanTAWSSaorta", "LSA (%)", "Alpha (degree)",
                "Dmax (cm)", "Aneurysm_volume (ml)", "Dmax_hyd/Dmin_hyd"]
 
dm = dg[selected_vars]
 
# Calculate correlation matrix and p-values for 11 variables
def correlation_with_pvalues(df):
    """Calculate correlation matrix with p-values"""
    n_vars = df.shape[1]
    corr_matrix = np.zeros((n_vars, n_vars))
    p_matrix = np.zeros((n_vars, n_vars))
    for i in range(n_vars):
        for j in range(n_vars):
            if i == j:
                corr_matrix[i, j] = 1.0
                p_matrix[i, j] = 0.0
            else:
                corr, p_val = pearsonr(df.iloc[:, i], df.iloc[:, j])
                corr_matrix[i, j] = corr
                p_matrix[i, j] = p_val
    return corr_matrix, p_matrix
 
correlation_matrix, p_matrix = correlation_with_pvalues(dm)
 
# Create correlation plot for 11 variables with Bonferroni correction
def plot_correlation_with_significance(corr_matrix, p_matrix, labels, sig_level, 
                                     filename, title="Correlation Matrix"):
    """Plot correlation matrix with significance testing"""
    # Create mask for non-significant correlations
    mask_nonsig = p_matrix >= sig_level
    # Create hierarchical clustering for ordering
    linkage_matrix = linkage(1 - np.abs(corr_matrix), method='ward')
    cluster_order = dendrogram(linkage_matrix, no_plot=True)['leaves']
    # Reorder matrices
    corr_ordered = corr_matrix[np.ix_(cluster_order, cluster_order)]
    mask_ordered = mask_nonsig[np.ix_(cluster_order, cluster_order)]
    labels_ordered = [labels[i] for i in cluster_order]
    # Create upper triangular mask
    mask_upper = np.triu(np.ones_like(corr_ordered, dtype=bool))
    mask_combined = mask_upper | mask_ordered
    plt.figure(figsize=(16, 10))
    # Create heatmap
    sns.heatmap(corr_ordered, 
                mask=mask_combined,
                annot=False,
                cmap='RdBu_r',
                center=0,
                square=True,
                xticklabels=labels_ordered,
                yticklabels=labels_ordered,
                cbar_kws={"shrink": 0.8})
    plt.title(title, fontsize=18)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
 
# Plot for 11 variables with Bonferroni correction
plot_correlation_with_significance(
    correlation_matrix, 
    p_matrix, 
    selected_vars, 
    bonf_thresh,
    r"C:\Users\magnuswe\OneDrive - SINTEF\Dokumenter\correlation_graph_11_var.pdf",
    "Correlation Matrix (11 variables, Bonferroni corrected)"
)
 
# Back to 17 variables with significance level = 0.05
# First create correlation table
dg_numeric = dg.select_dtypes(include=[np.number])  # Select only numeric columns
if dg_numeric.shape[1] < dg.shape[1] - 1:  # If we need to exclude first column manually
    dg_analysis = dg.iloc[:, 1:]  # Exclude first column
else:
    dg_analysis = dg_numeric
 
correlation_matrix_17 = dg_analysis.corr()
 
# Create lower triangular correlation table
correlation_table = correlation_matrix_17.copy()
correlation_table = correlation_table.where(np.tril(np.ones(correlation_table.shape), k=-1).astype(bool))
 
print("Correlation Table (17 variables):")
print(correlation_table)
 
# Calculate correlation and p-values for 17 variables
correlation_matrix_17_vals, p_matrix_17 = correlation_with_pvalues(dg_analysis)
 
# Plot correlation matrix for 17 variables with significance level = 0.05
def plot_correlation_with_coefficients(corr_matrix, p_matrix, labels, sig_level, filename):
    """Plot correlation matrix with coefficients and significance"""
    # Create mask for upper triangle and non-significant values
    mask_upper = np.triu(np.ones_like(corr_matrix, dtype=bool))
    mask_nonsig = p_matrix >= sig_level
    # Hierarchical clustering
    linkage_matrix = linkage(1 - np.abs(corr_matrix), method='ward')
    cluster_order = dendrogram(linkage_matrix, no_plot=True)['leaves']
    # Reorder
    corr_ordered = corr_matrix[np.ix_(cluster_order, cluster_order)]
    p_ordered = p_matrix[np.ix_(cluster_order, cluster_order)]
    labels_ordered = [labels[i] for i in cluster_order]
    mask_upper_ordered = mask_upper[np.ix_(cluster_order, cluster_order)]
    mask_nonsig_ordered = p_ordered >= sig_level
    plt.figure(figsize=(16, 10))
    # Create annotations matrix
    annot_matrix = np.where(mask_upper_ordered | mask_nonsig_ordered, '', 
                           np.round(corr_ordered, 2).astype(str))
    # Create heatmap
    sns.heatmap(corr_ordered,
                mask=mask_upper_ordered | mask_nonsig_ordered,
                annot=annot_matrix,
                fmt='',
                annot_kws={'size': 8},
                cmap='RdBu_r',
                center=0,
                square=True,
                xticklabels=labels_ordered,
                yticklabels=labels_ordered,
                cbar_kws={"shrink": 0.8})
    plt.title("Correlation Matrix (17 variables, p < 0.05)", fontsize=18)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
 
# Plot 17 variables correlation matrix
plot_correlation_with_coefficients(
    correlation_matrix_17_vals,
    p_matrix_17,
    list(dg_analysis.columns),
    0.05,
    r"C:\Users\magnuswe\OneDrive - SINTEF\Dokumenter\correlation_graph_17_var.pdf"
)
 
# Create scatter plot matrix (equivalent to chart.Correlation)
def create_scatter_matrix(df, title="Correlation Scatter Matrix"):
    """Create scatter plot matrix with histograms on diagonal"""
    n_vars = df.shape[1]
    fig, axes = plt.subplots(n_vars, n_vars, figsize=(20, 16))
    fig.suptitle(title, fontsize=16)
    for i in range(n_vars):
        for j in range(n_vars):
            ax = axes[i, j]
            if i == j:
                # Diagonal: histogram
                ax.hist(df.iloc[:, i], bins=20, alpha=0.7, edgecolor='black')
                ax.set_title(f'{df.columns[i]}', fontsize=8)
            else:
                # Off-diagonal: scatter plot
                ax.scatter(df.iloc[:, j], df.iloc[:, i], alpha=0.6, s=10)
                # Calculate and display correlation
                corr, p_val = pearsonr(df.iloc[:, j], df.iloc[:, i])
                ax.text(0.05, 0.95, f'r={corr:.3f}\np={p_val:.3f}', 
                       transform=ax.transAxes, fontsize=6,
                       verticalalignment='top',
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            # Set labels only on edges
            if i == n_vars - 1:
                ax.set_xlabel(df.columns[j], fontsize=8)
            if j == 0:
                ax.set_ylabel(df.columns[i], fontsize=8)
            ax.tick_params(labelsize=6)
    plt.tight_layout()
    plt.savefig(r"C:\Users\magnuswe\OneDrive - SINTEF\Dokumenter\scatter_matrix.pdf", dpi=300, bbox_inches='tight')
    plt.show()
 
# Create scatter matrix for all variables
create_scatter_matrix(dg_analysis, "Correlation Scatter Matrix (Pearson method)")
 
print(f"Bonferroni threshold: {bonf_thresh:.6f}")
print(f"Number of variables in analysis: {dg_analysis.shape[1]}")
print(f"Number of observations: {dg_analysis.shape[0]}")