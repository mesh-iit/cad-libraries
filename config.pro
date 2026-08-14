!
!   Default iCub CAD configuration file
!
!   created by: Luca Fiorio, Marcello Savoldi, Mattia Salvi, Michele Gesino
!
!   Version History
!   XX    YYYY/MM/DD   Author    Description
!   01    2019/09/23   Savoldi   modified to start migration to github
!   02    2019/10714   Gesino	 set "output dir" as folder for Creo Simulate Files
!   03    2019/10/28   Savoldi   set:   "ecad_export_holes_as_cuts" set as "yes"
!                                       "ecad_export_cuts_as_holes" set as "no"
!                                       "nmgr_outdated_mp" set as "do_not_show"
!   04    2019/09/24   Savoldi   modified default template for ECAD feature (asm and prt)
!   05    2020/02/14   Savoldi   Added modelcheck path and matlab string
!   06    2021/04/20   Savoldi   Added white background for render scene as default
!   07    2021/09/21   Protopapa Added "hole_parameter_file_path" as ".\config"
!   08    2021/10/28   Shah      Added "start_model_dir" as ".config\standard_files"

!
!
!
! Assembly ________________________________________________
!
freeze_failed_assy_comp yes
!
! Colors __________________________________________________
!
system_colors_file .\config\syscol.scl
!
! Data exchange ___________________________________________
!
! options for .pdf export
pdf_linecap round
pdf_linejoin round
pdf_use_pentable yes
!
! Dimensions & Tolerances _________________________________
!
! encloses reference dimensions in parentheses
parenthesize_ref_dim yes
tolerance_standard iso
!
! Drawing _________________________________________________
!
! default BOM format
bom_format .\config\bom_icub.fmt
drawing_setup_file .\config\std_fmt.dtl
dwg_unicode_conversion_language english
format_setup_file .\config\std_fmt.dtl
! create parameters if referenced by tables
make_parameters_from_fmt_tables yes
! setting directory of standard configuration files
pro_dtl_setup_dir .\config\
pro_format_dir .\config\drawing_formats
pro_symbol_dir .\config\symbols
todays_date_note_format %dd-%Mmm-%yy
! set "select to keep" the default behaviour in the drawing environment
show_preview_default keep
!
!Environment _________________________________________________
!
info_output_mode choose
pro_unit_length unit_mm
pro_unit_mass unit_kilogram
pro_unit_sys mmns
mass_property_calculate automatic
display_annotations no
!
! File Storage & Retrival _________________________________
!
!pro_library_dir .\commercial\objlib
pro_material_dir .\config\materials
rename_drawings_with_object both
save_dialog_for_existing_models yes
save_instance_accelerator ALWAYS
search_path_file .\config\search_path.pro
search_path_file .\config\search_path_custom.pro
template_designasm .\config\standard_files\start_asm.asm.1
template_drawing $PRO_DIRECTORY\templates\a3_drawing.drw
template_sheetmetalpart .\config\standard_files\sheetmetal_start_part.prt.1
template_solidpart .\config\standard_files\start_part.prt.1
!
! Layers __________________________________________________
!
!def_layer LAYER_DETAIL_ITEM detail
!def_layer LAYER_ASSEM_MEMBER components
!def_layer LAYER_COSM_SKETCH cosmetic
!def_layer LAYER_AXIS axis
!def_layer LAYER_SURFACE dsurf
!def_layer LAYER_DATUM dplane
!def_layer LAYER_POINT dpoint
!def_layer LAYER_CURVE dcurve
!def_layer LAYER_CSYS csys
!def_layer LAYER_HOLE_FEAT hole
!def_layer LAYER_ROUND_FEAT round
!def_layer LAYER_CHAMFER_FEAT chamfer
!def_layer LAYER_SLOT_FEAT slot
!def_layer LAYER_CUT_FEAT cut
!def_layer LAYER_PROTRUSION_FEAT protrusion
!def_layer LAYER_RIB_FEAT rib
!def_layer LAYER_DRAFT_FEAT draft
!def_layer LAYER_SHELL_FEAT shell
!def_layer LAYER_CORN_CHAMF_FEAT corn_chamfer
!def_layer LAYER_ASSY_CUT_FEAT assy_cut
!def_layer LAYER_DIM dimension
!def_layer LAYER_DRIVEN_DIM driven_dim
!def_layer LAYER_REFDIM refdim
!def_layer LAYER_NOTE note
!def_layer LAYER_GTOL gtol
!def_layer LAYER_SFIN finish
!def_layer LAYER_QUILT quilts
!def_layer LAYER_DWG_TABLE dwgtable
!def_layer layer_gtol geom_tol_datums
!
! Model Display ___________________________________________
!
display_axes YES
display_coord_sys NO
display_points no
display_planes no
! hide datum curves in shaded models
shade_with CURVES
! hide tags
display_axis_tags no
display_plane_tags YES
display_point_tags no
display_coord_sys_tags no
!
! Printing & Plotting ______________________________________
!
pen_table_file .\config\pen_table.pnt
!
! Sketcher _________________________________________________
!
!
sketcher_starts_in_2d yes
!
! System __________________________________________________
!
trail_dir .\config\trail
!
! User Interface __________________________________________
!
!mdl_tree_cfg_file .\config\tree.cfg
! options for keeping the English language
menu_translation no
dialog_translation no
help_translation no
msg_translation no
! enable feature recognition tool
frt_enabled yes
!
! Weld ____________________________________________________
!
weld_ui_standard iso
multiple_skeletons_allowed yes
default_ext_ref_scope skeleton_model
!
! Simulation _______________________________________________
!
sim_run_out_dir .\output_dir
sim_run_tmp_dir .\output_dir
!
!
! Mapkeys ____________________________________________________
!
mapkey z @MAPKEY_NAMEopen parameters window;@MAPKEY_LABELparameters;\
mapkey(continued) ~ Command `ProCmdMmParams`;
mapkey d @MAPKEY_NAMEmapkey for edit definition;@MAPKEY_LABELedit definition;\
mapkey(continued) ~ Command `ProCmdRedefine`;
mapkey e @MAPKEY_NAMEmapkey to edit the definition of features;\
mapkey(continued) @MAPKEY_LABELedit definition;\
mapkey(continued) ~ Command `ProCmdL05Edit@PopupMenuGraphicWinStack`;
mapkey w @MAPKEY_LABELselect parent;\
mapkey(continued) ~ Timer `UI Desktop` `UI Desktop` `popupMenuRMBTimerCB`;\
mapkey(continued) ~ Close `rmb_popup` `PopupMenu`;~ Activate `rmb_popup` `Selobj_parent`;
mapkey s @MAPKEY_NAMEmapkey for editing sketches;@MAPKEY_LABELedit sketch;\
mapkey(continued) ~ Command `ProCmdRedefine` ;\
mapkey(continued) ~ Activate `main_dlg_cur` `chkbn.revolve_1_placement.0` 1;\
mapkey(continued) ~ Activate `revolve_1_placement.0.0` `PH.Sketch`;\
mapkey(continued) ~ Activate `main_dlg_cur` `chkbn.extrev_1_placement.0` 1;\
mapkey(continued) ~ Activate `extrev_1_placement.0.0` `PH.Sketch`;\
mapkey(continued) ~ Activate `main_dlg_cur` `chkbn.plrib_settings.0` 1;\
mapkey(continued) ~ Activate `plrib_settings.1.0` `PH.sketchrepresentator_btn`;\
mapkey(continued) ~ Activate `main_dlg_cur` `maindashInst0.Sketch`;
mapkey f @MAPKEY_LABELFRONT VIEW;\
mapkey(continued) ~ Command `ProCmdNamedViewsGalSelect`  `FRONT`;
mapkey t @MAPKEY_LABELTOP VIEW;~ Command `ProCmdNamedViewsGalSelect`  `TOP`;
mapkey r @MAPKEY_LABELRIGHT VIEW;\
mapkey(continued) ~ Command `ProCmdNamedViewsGalSelect`  `RIGHT`;
mapkey m @MAPKEY_LABELmass_properties;\
mapkey(continued) ~ Activate `main_dlg_cur` `page_Analysis_control_btn` 1;\
mapkey(continued) ~ Command `ProCmdNaModelProperties`;
mapkey q @MAPKEY_NAMEmapkey to measure the distance between surfaces;\
mapkey(continued) @MAPKEY_LABELmeasure surface distance;~ Command `ProCmdNaMeasureDistance` ;\
mapkey(continued) ~ Select `main_dlg_cur` `Sst_bar.filter_list` 1 `10`;\
mapkey(continued) ~ Command `ProCmdSelFilterSet` 90;
!
! open drawing mapkey
!
mapkey save_minimal_model_tree ~ Command `ProCmdMdlTreeRetrieve` ;\
mapkey(continued) ~ Trail `UI Desktop` `UI Desktop` `DLG_PREVIEW_POST` `file_open`;\
mapkey(continued) ~ Activate `file_open` `Current Dir`;\
mapkey(continued) ~ Update `file_open` `Inputname` \
mapkey(continued) `public\\config\\macros_mapkeys\\open_drawing\\minimal_tree.cfg`;\
mapkey(continued) ~ Activate `file_open` `Inputname`;~ Select `main_dlg_cur` `appl_casc`;\
mapkey(continued) ~ Command `ProCmdMdlTreeSaveAsText`;\
mapkey(continued) ~ Update `inputname` `InpName` \
mapkey(continued) `public\\config\\macros_mapkeys\\open_drawing\\model_tree.txt`;\
mapkey(continued) ~ Activate `inputname` `InpName`;~ Command `ProCmdMdlTreeRetrieve` ;\
mapkey(continued) ~ Trail `UI Desktop` `UI Desktop` `DLG_PREVIEW_POST` `file_open`;\
mapkey(continued) ~ Activate `file_open` `Current Dir`;\
mapkey(continued) ~ Update `file_open` `Inputname` `public\\config\\tree.cfg`;\
mapkey(continued) ~ Activate `file_open` `Inputname`;
mapkey load_drawing_mapkey ~ Select `main_dlg_cur` `appl_casc`;\
mapkey(continued) ~ Close `main_dlg_cur` `appl_casc`;~ Command `ProCmdRibbonOptionsDlg` ;\
mapkey(continued) ~ Select `ribbon_options_dialog` `PageSwitcherPageList` 1 `ConfigLayout`;\
mapkey(continued) ~ Select `ribbon_options_dialog` `ConfigLayout.ImportExportBtn`;\
mapkey(continued) ~ Close `ribbon_options_dialog` `ConfigLayout.ImportExportBtn`;\
mapkey(continued) ~ Activate `ribbon_options_dialog` `ConfigLayout.Open`;\
mapkey(continued) ~ Activate `file_open` `Current Dir`;\
mapkey(continued) ~ Update `file_open` `Inputname` \
mapkey(continued) `public\\config\\macros_mapkeys\\open_drawing\\open_drawing_mapkey.pro`;\
mapkey(continued) ~ Command `ProFileSelPushOpen_Standard@context_dlg_open_cmd` ;\
mapkey(continued) ~ Activate `ribbon_options_dialog` `OkPshBtn`;\
mapkey(continued) ~ FocusIn `UITools Msg Dialog Future` `no`;\
mapkey(continued) ~ Activate `UITools Msg Dialog Future` `no`;
mapkey run_drawing_script @SYSTEMpowershell -File \
mapkey(continued) .\\public\\config\\macros_mapkeys\\open_drawing\\drawing.ps1;
mapkey clean-up @SYSTEMpowershell -command "& {& 'Remove-Item' \
mapkey(continued) ".\\public\\config\\macros_mapkeys\\open_drawing\\model_tree.txt"}"\;\
mapkey(continued) "& {& 'Remove-Item' \
mapkey(continued) ".\\public\\config\\macros_mapkeys\\open_drawing\\open_drawing_mapkey.pro"}";
mapkey $F12 %save_minimal_model_tree;%run_drawing_script;~;\
mapkey(continued) %load_drawing_mapkey;%clean-up;%open_drawing_mapkey;



!
! Commented but useful _______________________________________
!
! when opening files start from the working_dir
!file_open_default_folder working_directory
! addtional absolute path for automatic drawing generation with distributed Pro/Batch
!search_path (null)
!mapkey  e @MAPKEY_LABELedit;\
mapkey(continued) ~ Timer `UI Desktop` `UI Desktop` `popupMenuRMBTimerCB`;\
mapkey(continued) ~ Close `rmb_popup` `PopupMenu`;~ Activate `rmb_popup` `L05Edit`;
!mapkey  a @MAPKEY_LABELDATUMS ON;~ Command `ProCmdEnvAxisDisp` 1;\
mapkey(continued) ~ Command `ProCmdEnvPntsDisp` 1;~ Command `ProCmdEnvCsysDisp` 1;\
mapkey(continued) ~ Command `ProCmdEnvDtmDisp` 1;
!mapkey  q @MAPKEY_LABELDATUMS OFF;~ Activate `main_dlg_cur`; `all_check` 1;
!mapkey  plpl @!mapkey_LABELplane to plane distance;\
mapkey(continued) ~ Command `ProCmdNaMeasureDistance` ;\
mapkey(continued) ~ Close `main_dlg_cur` `Analysis.cas_na_measure`;\
mapkey(continued) ~ Open `main_dlg_cur` `Sst_bar.filter_list`;\
mapkey(continued) ~ Close `main_dlg_cur` `Sst_bar.filter_list`;\
mapkey(continued) ~ Select `main_dlg_cur` `Sst_bar.filter_list`1 `13`;\
mapkey(continued) ~ Command `ProCmdSelFilterSet` 90;
!mapkey  axax @!mapkey_LABELaxis to axis distance;\
mapkey(continued) ~ Command `ProCmdNaMeasureDistance` ;\
mapkey(continued) ~ Close `main_dlg_cur` `Analysis.cas_na_measure`;\
mapkey(continued) ~ Open `main_dlg_cur` `Sst_bar.filter_list`;\
mapkey(continued) ~ Close `main_dlg_cur` `Sst_bar.filter_list`;\
mapkey(continued) ~ Select `main_dlg_cur` `Sst_bar.filter_list`1 `9`;\
mapkey(continued) ~ Command `ProCmdSelFilterSet` 15;
!mapkey  dxf2workdir @!mapkey_NAMEsave a .dxf of the current drawing in the \
mapkey(continued) working directory;@!mapkey_LABELsave .dxf file to working dir;\
mapkey(continued) ~ Command `ProCmdModelSaveAs` ;~ Activate `file_saveas` `Current Dir`;\
mapkey(continued) ~ Open `file_saveas` `type_option`;~ Close `file_saveas` `type_option`;\
mapkey(continued) ~ Select `file_saveas` `type_option` 1 `db_137`;\
mapkey(continued) ~ Activate `file_saveas` `OK`;~ Activate `export_2d_dlg` `OK_Button`;`;
!mapkey  savetree @!mapkey_NAMEsave the model tree to the working direcotry \
mapkey(continued) as treetool.txt;@!mapkey_LABELexport treetool.txt;\
mapkey(continued) ~ Command `ProCmdMdlTreeRetrieve` ;\
mapkey(continued) ~ Trail `UI Desktop` `UI Desktop` `DLG_PREVIEW_POST` `file_open`;\
mapkey(continued) ~ Select `file_open` `Ph_list.Filelist` 1 `config`;\
mapkey(continued) ~ Select `file_open` `Ph_list.Filelist` 1 `config`;\
mapkey(continued) ~ Activate `file_open` `Ph_list.Filelist` 1 `config`;\
mapkey(continued) ~ Select `file_open` `Ph_list.Filelist` 1 `tree.cfg`;\
mapkey(continued) ~ Activate `file_open` `Ph_list.Filelist` 1 `tree.cfg`;\
mapkey(continued) ~ Command `ProCmdMdlTreeSaveAsText` ;~ Activate `inputname` `okbutton`;\
mapkey(continued) ~ Command `ProCmdMdlTreeColumns` ;~ Activate `column` `RmvBtn`;\
mapkey(continued) ~ Activate `column` `OKBtn`;
!mapkey  dxf2prodoc @!mapkey_NAMEcopy a .dxf drawing to the production \
mapkey(continued) documents folder and rename it appending its revision number;\
mapkey(continued) @!mapkey_LABELcopy .dxf to prodoc;\
mapkey(continued) @SYSTEMprivate\\utils\\batchScripts\\saveDxfToProdoc.bat;
!mapkey  dxf_w_rev @!mapkey_NAMEsave a .dxf file to the production documents \
mapkey(continued) folder and rename it appending its revision number;\
mapkey(continued) @!mapkey_LABELsave .dxf to prodoc;%savetree;%dxf2workdir;%dxf2prodoc;
!mapkey  stl2prodoc @!mapkey_NAMEcopy a .stl file to the production documents \
mapkey(continued) folder and rename it appending its revision number;\
mapkey(continued) @!mapkey_LABELcopy .stl to prodoc;\
mapkey(continued) @SYSTEMprivate\\utils\\batchScripts\\saveStlToProdoc.bat;
!mapkey  stl_w_rev @!mapkey_NAMEsave a .stl file to the production documents \
mapkey(continued) folder and rename it appending its revision number;\
mapkey(continued) @!mapkey_LABELsave .stl to prodoc;%savetree;%stl2workdir;%stl2prodoc;
!mapkey  stl2workdir @!mapkey_LABELsave .stl file to working dir;\
mapkey(continued) ~ Command `ProCmdModelSaveAs` ;~ Activate `file_saveas` `Current Dir`;\
mapkey(continued) ~ Open `file_saveas` `type_option`;~ Close `file_saveas` `type_option`;\
mapkey(continued) ~ Select `file_saveas` `type_option` 1 `db_549`;\
mapkey(continued) ~ Activate `file_saveas` `OK`;~ Update `export_slice` `ChordHeightPanel` `0`;\
mapkey(continued) ~ Activate `export_slice` `ChordHeightPanel`;\
mapkey(continued) ~ FocusOut `export_slice` `ChordHeightPanel`;\
mapkey(continued) ~ Update `export_slice` `AngleControlPanel` `1`;\
mapkey(continued) ~ FocusOut `export_slice` `AngleControlPanel`;~ Activate `export_slice` `OK`;\
mapkey(continued) ~ Command `ProCmdViewRepaint`;

!
! Other options ______________________________________________
!
! do not show family table instances when opening files
menu_show_instances no
!display text of selected items
provide_pick_message_always yes
tol_display yes
2d_palette_path .\config\custom_sketches
save_model_display shading_low
spin_center_display no
remember_replaced_components no
regen_solid_before_save yes

ecad_comp_naming_convention ecad_alt_name
search_area_for_comp_interfaces 99
intf2d_out_enhanced_ents none
export_profiles_step .\config\def_profile.dep_step
intf3d_out_configure_export yes
ecad_export_holes_as_cuts yes
ecad_export_cuts_as_holes no
nmgr_outdated_mp do_not_show
template_new_ecadasm .\config\standard_files\start_asm_ecad.asm
template_boardpart .\config\standard_files\start_part_ecad.prt

! Modelcheck strings:
modelcheck_dir .\config\modelcheck

! SimMechanics link
!toolkit_registry_file .\config\matlab\creolink.dat

default_scene_filename .\config\render_scene\IIT_default_scene.scn
hole_parameter_file_path .\config
hole_file_resolution replace_with_external
pro_surface_finish_dir .\config\symbols\surf_finish

start_model_dir .\config\standard_files
display shadewithedges
pro_table_dir .\config\tables
open_simplified_rep_by_default Last Stored
orientation isometric
