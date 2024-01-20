open_project test
set_top $env(KERNEL)
add_files ../../$env(SOURCE)
open_solution "solution1" -flow_target vivado
set_part $env(PART)
create_clock -period $env(HLS_PERIOD) -name default
config_export -format ip_catalog -rtl verilog -vivado_clock $env(VIVADO_PERIOD) -vivado_phys_opt all
config_export -vivado_synth_strategy=$env(SYNTH_STRATEGY)
config_export -vivado_impl_strategy=$env(IMPL_STRATEGY)
set_clock_uncertainty 0
csynth_design
export_design -flow impl -rtl verilog -format ip_catalog
close_project
exit
