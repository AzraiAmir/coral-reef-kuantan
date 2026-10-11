@echo off
REM === Azr.AI - Reorganize flat GitHub files into proper folders ===

echo Creating folder structure...
mkdir src 2>nul
mkdir src\data_acquisition 2>nul
mkdir src\preprocessing 2>nul
mkdir src\detection 2>nul
mkdir src\health_assessment 2>nul
mkdir src\connectivity 2>nul
mkdir src\environmental 2>nul
mkdir src\spatial_analysis 2>nul
mkdir src\validation 2>nul
mkdir src\visualization 2>nul
mkdir src\standards 2>nul
mkdir src\utils 2>nul
mkdir scripts 2>nul
mkdir tests 2>nul
mkdir configs 2>nul
mkdir data 2>nul
mkdir data\raw 2>nul
mkdir data\raw\test_images 2>nul
mkdir data\raw\test_videos 2>nul
mkdir data\processed 2>nul
mkdir data\annotations 2>nul
mkdir data\metadata 2>nul
mkdir data\external 2>nul
mkdir models 2>nul
mkdir models\pretrained 2>nul
mkdir models\trained 2>nul
mkdir models\trained\yolov8_coral 2>nul
mkdir models\trained\yolov8_coral\weights 2>nul
mkdir results 2>nul
mkdir results\figures 2>nul
mkdir results\tables 2>nul
mkdir results\maps 2>nul
mkdir results\detections 2>nul
mkdir results\health 2>nul
mkdir notebooks 2>nul
mkdir docs 2>nul

echo Creating __init__.py files...
type nul > src\__init__.py
type nul > src\data_acquisition\__init__.py
type nul > src\preprocessing\__init__.py
type nul > src\detection\__init__.py
type nul > src\health_assessment\__init__.py
type nul > src\connectivity\__init__.py
type nul > src\environmental\__init__.py
type nul > src\spatial_analysis\__init__.py
type nul > src\validation\__init__.py
type nul > src\visualization\__init__.py
type nul > src\standards\__init__.py
type nul > src\utils\__init__.py
type nul > tests\__init__.py

echo Moving files into place...

REM --- F: Data Acquisition ---
move adcp_processor.py src\data_acquisition\ 2>nul
move ctd_processor.py src\data_acquisition\ 2>nul
move data_loader.py src\data_acquisition\ 2>nul
move image_logger.py src\data_acquisition\ 2>nul
move metadata_manager.py src\data_acquisition\ 2>nul
move spawning_logger.py src\data_acquisition\ 2>nul

REM --- G: Preprocessing ---
move annotation_conversion.py src\preprocessing\ 2>nul
move annotation_manager.py src\preprocessing\ 2>nul
move augmentation.py src\preprocessing\ 2>nul
move class_distribution.py src\preprocessing\ 2>nul
move dataset_splitter.py src\preprocessing\ 2>nul
move deep_multiscale_fusion.py src\preprocessing\ 2>nul
move dl_enhancement.py src\preprocessing\ 2>nul
move enhancement_comparison.py src\preprocessing\ 2>nul
move enhancement_metrics.py src\preprocessing\ 2>nul
move image_enhancement_batch.py src\preprocessing\ 2>nul
move inter_annotator_agreement.py src\preprocessing\ 2>nul
move quality_control.py src\preprocessing\ 2>nul
move traditional_enhancement.py src\preprocessing\ 2>nul

REM --- H: Detection ---
move bias_mitigation.py src\detection\ 2>nul
move confusion_matrix.py src\detection\ 2>nul
move coralscop_segmentation.py src\detection\ 2>nul
move mask_quality_control.py src\detection\ 2>nul
move model_comparison.py src\detection\ 2>nul
move model_inference.py src\detection\ 2>nul
move precision_recall_curves.py src\detection\ 2>nul
move segmentation_metrics.py src\detection\ 2>nul
move training_curves.py src\detection\ 2>nul
move xai_interpretability.py src\detection\ 2>nul
move yolov8_ablation.py src\detection\ 2>nul
move yolov8_detector.py src\detection\ 2>nul
move yolov8_hyperparameter_tuning.py src\detection\ 2>nul

REM --- I: Health Assessment ---
move bleaching_severity_map.py src\health_assessment\ 2>nul
move coral_crca.py src\health_assessment\ 2>nul
move coral_crca_calibration.py src\health_assessment\ 2>nul
move coral_health_visualization.py src\health_assessment\ 2>nul
move d_to_white.py src\health_assessment\ 2>nul
move disease_detection.py src\health_assessment\ 2>nul
move disease_detection_training.py src\health_assessment\ 2>nul
move kbi_calculator.py src\health_assessment\ 2>nul

REM --- I: Connectivity ---
move connectivity_visualization.py src\connectivity\ 2>nul
move dpi_calculator.py src\connectivity\ 2>nul
move genetic_validation.py src\connectivity\ 2>nul
move mike21_boundary_conditions.py src\connectivity\ 2>nul
move mike21_extract_results.py src\connectivity\ 2>nul
move mike21_mesh_generation.py src\connectivity\ 2>nul
move mike21_run_simulation.py src\connectivity\ 2>nul
move mike21_setup.py src\connectivity\ 2>nul
move mike21_validation.py src\connectivity\ 2>nul
move particle_tracking.py src\connectivity\ 2>nul

REM --- J: Spatial Analysis ---
move correlation_analysis.py src\spatial_analysis\ 2>nul
move debris_mapping.py src\spatial_analysis\ 2>nul
move environmental_correlation.py src\spatial_analysis\ 2>nul
move gis_mapping.py src\spatial_analysis\ 2>nul
move habitat_mapping.py src\spatial_analysis\ 2>nul
move regression_analysis.py src\spatial_analysis\ 2>nul
move spatial_interpolation.py src\spatial_analysis\ 2>nul
move statistical_analysis.py src\spatial_analysis\ 2>nul
move temporal_trend_analysis.py src\spatial_analysis\ 2>nul
move zonation_algorithm.py src\spatial_analysis\ 2>nul

REM --- J: Validation ---
move model_validation.py src\validation\ 2>nul

REM --- J: Visualization ---
move connectivity_network.py src\visualization\ 2>nul
move dashboard.py src\visualization\ 2>nul
move dashboard_pages.py src\visualization\ 2>nul

REM --- K: Utils ---
move config_loader.py src\utils\ 2>nul
move data_versioning.py src\utils\ 2>nul
move reproducibility.py src\utils\ 2>nul

echo.
echo ===================================
echo Reorganization complete!
echo ===================================
echo.
echo Python files now under src:
dir /s /b src\*.py | find /c ".py"