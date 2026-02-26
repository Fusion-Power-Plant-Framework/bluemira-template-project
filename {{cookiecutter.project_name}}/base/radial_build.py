from __future__ import annotations

from typing import TYPE_CHECKING

from bluemira.codes import systems_code_solver
from bluemira.codes.process.api import Impurities
from bluemira.codes.process.equation_variable_mapping import Constraint, Objective
from bluemira.codes.process.model_mapping import (
    AlphaPressureModel,
    AvailabilityModel,
    BetaLimitModel,
    BootstrapCurrentScalingLaw,
    ConfinementTimeScalingLaw,
    CostModel,
    CSSuperconductorModel,
    CurrentDriveEfficiencyModel,
    DensityLimitModel,
    OperationModel,
    OutputCostsSwitch,
    PFSuperconductorModel,
    PlasmaCurrentScalingLaw,
    PlasmaGeometryModel,
    PlasmaNullConfigurationModel,
    PlasmaPedestalModel,
    PowerFlowModel,
    PrimaryPumpingModel,
    PROCESSOptimisationAlgorithm,
    SecondaryCycleModel,
    ShieldThermalHeatUse,
    TFNuclearHeatingModel,
    TFSuperconductorModel,
)
from bluemira.codes.process.template_builder import PROCESSTemplateBuilder

if TYPE_CHECKING:
    from bluemira.base.parameter_frame import ParameterFrame

template_builder = PROCESSTemplateBuilder()
template_builder.set_optimisation_algorithm(PROCESSOptimisationAlgorithm.VMCON)
template_builder.set_optimisation_numerics(maxiter=100, tolerance=1e-7)

template_builder.set_minimisation_objective(Objective.MAJOR_RADIUS)

for eq_constraint in (
    Constraint.BETA_CONSISTENCY,
    Constraint.GLOBAL_POWER_CONSISTENCY,
    Constraint.RADIAL_BUILD_CONSISTENCY,
):
    template_builder.add_constraint(eq_constraint, equality=True)

for ieq_constraint in (
    Constraint.PINJ_UPPER_LIMIT,
    Constraint.LH_THRESHHOLD_LIMIT,
    Constraint.NET_ELEC_LOWER_LIMIT,
    Constraint.BETA_UPPER_LIMIT,
    Constraint.PEAK_TF_UPPER_LIMIT,
    Constraint.CS_EOF_DENSITY_LIMIT,
    Constraint.CS_BOP_DENSITY_LIMIT,
    Constraint.TF_JCRIT_RATIO_UPPER_LIMIT,
    Constraint.TF_DUMP_VOLTAGE_UPPER_LIMIT,
    Constraint.TF_CURRENT_DENSITY_UPPER_LIMIT,
    Constraint.TF_T_MARGIN_LOWER_LIMIT,
    Constraint.CS_T_MARGIN_LOWER_LIMIT,
    Constraint.CONFINEMENT_RATIO_LOWER_LIMIT,
    Constraint.DUMP_TIME_LOWER_LIMIT,
    Constraint.CS_STRESS_UPPER_LIMIT,
    Constraint.DENSITY_PROFILE_CONSISTENCY,
    Constraint.PSEPB_QAR_UPPER_LIMIT,
    Constraint.TF_CASE_STRESS_UPPER_LIMIT,
    Constraint.TF_JACKET_STRESS_UPPER_LIMIT,
    Constraint.DENSITY_UPPER_LIMIT,
    Constraint.NWL_UPPER_LIMIT,
    Constraint.FUSION_POWER_UPPER_LIMIT,
    Constraint.BURN_TIME_LOWER_LIMIT,
):
    template_builder.add_constraint(ieq_constraint)

# Variable vector values and bounds
template_builder.add_variable("beta_total_vol_avg", 0.03)
template_builder.add_variable("j_cs_flat_top_end", 1.5e7)
template_builder.add_variable("nd_plasma_electrons_vol_avg", 7.5e19)
template_builder.add_variable("b_plasma_toroidal_on_axis", 5.7)

template_builder.add_variable("rmajor", 8.0, upper_bound=9, lower_bound=8)
template_builder.add_variable(
    "temp_plasma_electron_vol_avg_kev", 12.0, upper_bound=100.0
)
template_builder.add_variable("hfact", 1.1, upper_bound=1.2)
template_builder.add_variable("dr_cs", 0.5, lower_bound=0.3)
template_builder.add_variable("q95", 3.5, lower_bound=3)
template_builder.add_variable("dr_bore", 2.0, lower_bound=0.1)
template_builder.add_variable("f_c_plasma_non_inductive", 0.4)
template_builder.add_variable("t_tf_superconductor_quench", 25)
template_builder.add_variable("dr_tf_nose_case", 0.5)
template_builder.add_variable("dx_tf_turn_steel", 0.008, lower_bound=0.008)
template_builder.add_variable(
    "f_a_tf_turn_cable_copper", 0.8, upper_bound=0.94, lower_bound=0.5
)
template_builder.add_variable("c_tf_turn", 65000, upper_bound=90000, lower_bound=65000)
template_builder.add_variable("f_nd_alpha_electron", upper_bound=0.1)
template_builder.add_variable("f_a_cs_turn_steel", 0.8)
template_builder.add_variable("f_nd_impurity_electrons(13)", 3.8e-4)
template_builder.add_variable("dr_tf_wp_with_insulation", 0.5, lower_bound=0.4)

template_builder.add_impurity(Impurities.H, 0.9)
template_builder.add_impurity(Impurities.He, 0.1)
template_builder.add_impurity(Impurities.Xe, 3.8e-4)
template_builder.add_impurity(Impurities.W, 5.0e-6)

# Set model switches
for model_choice in (
    PlasmaGeometryModel.HENDER_K_D_100,
    BootstrapCurrentScalingLaw.SAUTER,
    BetaLimitModel.THERMAL,
    PlasmaCurrentScalingLaw.ITER_REVISED,
    DensityLimitModel.GREENWALD,
    AlphaPressureModel.WARD,
    PlasmaPedestalModel.PEDESTAL_GW,
    ConfinementTimeScalingLaw.IPB98_Y2_H_MODE,
    PlasmaNullConfigurationModel.SINGLE_NULL,
    OperationModel.PULSED,
    CurrentDriveEfficiencyModel.ECRH_UI_GAM,
    PowerFlowModel.SIMPLE,
    PrimaryPumpingModel.PRESSURE_DROP_INPUT,
    SecondaryCycleModel.INPUT,
    ShieldThermalHeatUse.LOW_GRADE_HEAT,
    TFNuclearHeatingModel.INPUT,
    OutputCostsSwitch.NO,
    CostModel.TETRA_1990,
    AvailabilityModel.INPUT,
    PFSuperconductorModel.NBTI,
    CSSuperconductorModel.NB3SN_ITER_STD,
    TFSuperconductorModel.NB3SN_ITER_STD,
):
    template_builder.set_model(model_choice)


# Set fixed input values
template_builder.add_input_values({
    "pulsetimings": 0,
    "p_hcd_injected_max": 200.0,
    "p_plant_electric_net_required_mw": 400.0,
    "b_tf_inboard_max": 14.0,
    "fjohc": 1.0,
    "f_j_cs_start_pulse_end_flat_top": 1.0,
    "fjohc0": 1.0,
    "fiooic": 1.0,
    "v_tf_coil_dump_quench_max_kv": 10.0,
    "tmargmin": 1.5,
    "temp_cs_superconductor_margin_min": 1.5,
    "f_alpha_energy_confinement_min": 5.0,
    "alstroh": 7.5e8,
    "psepbqarmax": 10.0,
    "sig_tf_case_max": 7.5e8,
    "sig_tf_wp_max": 7.5e8,
    "fdene": 1.2,
    "pflux_fw_neutron_max_mw": 2.0,
    "p_fusion_total_max_mw": 3000,
    "t_burn_min": 7200.0,
    "dr_shld_thermal_inboard": 0.050,
    "dr_shld_thermal_outboard": 0.050,
    "dz_shld_thermal": 0.050,
    "dr_shld_vv_gap_inboard": 0.02,
    "dr_vv_inboard": 0.3,
    "dr_vv_outboard": 0.3,
    "dz_vv_upper": 0.3,
    "dz_vv_lower": 0.3,
    "dr_shld_inboard": 0.3,
    "dr_shld_blkt_gap": 0.02,
    "dr_blkt_inboard": 0.7,
    "dr_fw_plasma_gap_inboard": 0.25,
    "dr_fw_plasma_gap_outboard": 0.25,
    "dr_blkt_outboard": 1.0,
    "dr_cryostat": 0.15,
    "dr_shld_outboard": 0.800,
    "dz_divertor": 0.62,
    "i_div_heat_load": 2,
    "vfshld": 0.60,
    "aspect": 3.0,
    "f_nd_plasma_separatrix_greenwald": 0.5,
    "nd_plasma_pedestal_electron": 0.5e20,
    "nd_plasma_separatrix_electron": 0.2e20,
    "radius_plasma_pedestal_density_norm": 0.94,
    "radius_plasma_pedestal_temp_norm": 0.94,
    "tbeta": 2.0,
    "temp_plasma_pedestal_kev": 5.5,
    "temp_plasma_separatrix_kev": 0.1,
    "kappa": 1.85,
    "triang": 0.5,
    "alphan": 1.00,
    "alphat": 1.45,
    "beta_norm_max": 3.0,
    "fkzohm": 1.02,
    "ejima_coeff": 0.3,
    "q0": 1.0,
    "f_sync_reflect": 0.6,
    "plasma_res_factor": 0.7,
    "t_plant_pulse_dwell": 1800.0,
    "t_plant_pulse_coil_precharge": 500.0,
    "f_c_plasma_bootstrap_max": 0.95,
    "eta_cd_norm_ecrh": 0.30,
    "eta_ecrh_injector_wall_plug": 0.5,
    "p_hcd_primary_extra_heat_mw": 75.0,
    "radius_plasma_core_norm": 0.75,
    "f_p_plasma_core_rad_reduction": 0.6,
    "eta_coolant_pump_electric": 0.87,
    "etaiso": 0.9,
    "eta_turbine": 0.4,
    "qnuc": 1.3e4,
    "f_t_plant_available": 0.80,
    "c_pf_coil_turn_peak_input": [4e4, 4e4, 4e4, 4e4, 4e4, 4e4, 4e4, 4e4],
    "i_pf_location": [2, 2, 3, 3],
    "n_pf_coils_in_group": [1, 1, 2, 2],
    "n_pf_coil_groups": 4,
    "f_z_cs_tf_internal": 0.9,
    "j_pf_coil_wp_peak": [1.1e7, 1.1e7, 6.0e6, 6.0e6, 8.0e6, 8.0e6, 8.0e6, 8.0e6],
    "rpf2": -1.825,
    "zref": [3.6, 1.2, 1.0, 2.8, 1.0, 1.0, 1.0, 1.0],
    "fcuohsu": 0.70,
    "dr_tf_plasma_case": 0.06,
    "dx_tf_side_case_min": 0.05,
    "ripple_b_tf_plasma_edge_max": 0.6,
    "n_tf_coils": 16,
    "dx_tf_wp_insulation": 0.008,
    "dia_tf_turn_coolant_channel": 0.01,
    "tftmp": 4.75,
    "f_a_tf_turn_cable_space_extra_void": 0.3,
    "nflutfmax": 1e22,
})


def radial_build(params: ParameterFrame, build_config: dict) -> ParameterFrame:
    """Update parameters after a radial build is run/read/mocked using PROCESS.

    Parameters
    ----------
    params:
        Parameters on which to perform the solve (updated)
    build_config:
        Build configuration

    Returns
    -------
    Updated parameters following the solve.
    """
    run_mode = build_config.pop("run_mode", "mock")
    plot = build_config.pop("plot", False)

    if run_mode == "run":
        template_builder.set_run_title(
            build_config.pop(
                "PROCESS_runtitle", "Bluemira {{cookiecutter.project_name}}"
            )
        )
        build_config["template_in_dat"] = template_builder.make_inputs()
    solver = systems_code_solver(params, build_config)

    solver.params.update_mappings({
        "e_nbi": {"send": False},
        "eta_nb": {"send": False},
        "e_mult": {"send": False},
        "m_s_limit": {"send": False},
        "bb_t_inlet": {"send": False},
        "bb_t_outlet": {"send": False},
        "rrr_tf_cu": {"send": False},
        "t_tf_quench_detection": {"send": False},
        "g_cs_tf": {"send": False},
        "g_ts_tf": {"send": False},
    })
    new_params = solver.execute(run_mode)

    if plot:
        solver.plot_radial_build(show=True)
    params.update_from_frame(new_params)
    return params
