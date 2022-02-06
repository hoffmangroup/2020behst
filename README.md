### Fig 1. Extension Parameter
Run `python3 extension_parameter.py`

### Fig 3. Precision-Recall
Run `python3 precision_recall_plot_2022.py` or use the notebook `precision_recall_plot_2022.ipynb`

### Fig 4. Heatmap of Limb GO Terms
Run `python3 term_comparison_heatmap_2022.py` or use the notebook `term_comparison_heatmap_2022.ipynb`  
Note: Default plot only considers terms with source of GO:BP. To plot terms of both GO:BP and GO:MF, use `read_data(only_BP=False)`.

### Fig 5. EnrichmentMap for UK Biobank GWAS Data (Basophil)
Open Cytoscape session file `basophil_gobp_2022.cys` with Cytoscape.Versions used: 
  - Cytoscape 3.9.1
  - EnrichmentMap Pipeline Collection 1.1.0 (EnrichmentMap 3.3.3, AutoAnnotate 1.3.5, WordCloud 3.1.4, clusterMaker2 2.0)  

The session file is generated using the two files in `data/enrichment_map` with default settings.  
EnrichmentMap tutorial: https://baderlab.github.io/CBW_Pathways_2020/gprofiler-mod3.html#gprofiler_mod3
