template_owner_name_key = "owner"
template_project_name_key = "name"
template_root_node_name = "Root"

template_experiment_node_meta = "ExperimentIndex"
template_lec_node_meta = "LEC"
template_lec_node_model_blob ="model"

template_lec_exec_node_meta = "LECExec"
template_lec_exec_node_pointer = "LEC"
template_lec_file_name_key = "LEC_file_name"


template_NN_exec_node_meta = "NNModel"
template_NN_exec_node_pointer = "NN"
template_NN_node_base_meta = "NNType"

template_dataset_exec_node_meta = "DatasetSelect"
template_dataset_exec_node_pointer = "DD"
template_dataset_node_base_meta = "Dataset"




template_NN_CNN_key = "CNN"
template_NN_FFNN_key = "FFNN"
template_NN_NNCS_DiscreteLinear_key = "DiscreteLinearNNCS"
template_NN_NNCS_ContinuousLinear_key  = "ContinuousLinearNNCS"
template_NN_NNCS_DiscreteNonLinear_key = "DiscreteNonLinearNNCS"
template_NN_NNCS_ContinuousNonLinear_key = "ContinuousNonLinearNNCS"

template_NN_node_valid_meta = {
    template_NN_CNN_key ,
    template_NN_FFNN_key,
    template_NN_NNCS_DiscreteLinear_key,
    template_NN_NNCS_ContinuousLinear_key,
    template_NN_NNCS_DiscreteNonLinear_key,
    template_NN_NNCS_ContinuousNonLinear_key
}

template_CNN_attack_key = "attack"
template_CNN_delta_key = "delta"
template_CNN_target_key = "im_target"
template_CNN_mean_key = "mean"
template_CNN_pixels_key = "pixels"
template_CNN_reachability_method_key = "reach-method"
template_CNN_std_delta_key = "std"
template_CNN_threshold_key = "threshold"

template_CNN_param_keys = {
template_CNN_attack_key,template_CNN_delta_key,template_CNN_target_key,template_CNN_mean_key,template_CNN_pixels_key,
template_CNN_reachability_method_key, template_CNN_std_delta_key,template_CNN_threshold_key
}

template_FFNN_halfspace_matrix_key = "HalfSpace-matrix"
template_FFNN_halfspace_vector_key = "HalfSpace-vector"
template_FFNN_lb_key= "lb"
template_FFNN_ub_key  = "ub"
template_FFNN_reachability_key = "reach"
template_FFNN_verification_key  = "verify"
template_FFNN_reachability_method_key = "reach-method"

template_FFNN_param_keys = {
    template_FFNN_halfspace_matrix_key ,
    template_FFNN_halfspace_vector_key,
    template_FFNN_lb_key,
    template_FFNN_ub_key  ,
    template_FFNN_reachability_key ,
    template_FFNN_verification_key ,
    template_FFNN_reachability_method_key
}

template_NNCS_halfspace_matrix_key = "HalfSpace-matrix"
template_NNCS_halfspace_vector_key = "HalfSpace-vector"
template_NNCS_lb_key = "lb"
template_NNCS_ub_key = "ub"
template_NNCS_reachability_key = "reach"
template_NNCS_cores_key = "cores"
template_NNCS_steps = "steps"
template_NNCS_lb_refinput_key = "lb-refInput"
template_NNCS_ub_refinput_key= "ub-refInput"
template_NNCS_verification_key = "verify"
template_NNCS_reach_method_key = "reach-method"


template_NNCS_param_keys = {
    template_NNCS_halfspace_matrix_key,
    template_NNCS_halfspace_vector_key ,
    template_NNCS_lb_key,
    template_NNCS_ub_key ,
    template_NNCS_reachability_key,
    template_NNCS_cores_key,
    template_NNCS_steps,
    template_NNCS_lb_refinput_key ,
    template_NNCS_ub_refinput_key,
    template_NNCS_verification_key,
    template_NNCS_reach_method_key
}

template_NNCS_LinearSys_A_key = "A"
template_NNCS_LinearSys_B_key ="B"
template_NNCS_LinearSys_C_key ="C"
template_NNCS_LinearSys_D_key = "D"
template_NNCS_LinearSys_Ts_key  = "Ts"
template_NNCS_LinearSys_Cont_reachable_steps_key = "reachable-steps"

template_NNCS_LinearSys_param_keys = template_NNCS_param_keys.union({
template_NNCS_LinearSys_A_key,
template_NNCS_LinearSys_B_key ,
template_NNCS_LinearSys_C_key ,
template_NNCS_LinearSys_D_key ,
template_NNCS_LinearSys_Ts_key ,

})

template_NNCS_LinearSys_Cont_param_keys = template_NNCS_LinearSys_param_keys.union({
    template_NNCS_LinearSys_Cont_reachable_steps_key
})

template_NNCS_LinearSys_Discrete_param_keys = template_NNCS_LinearSys_param_keys



template_NNCS_NonLinearSys_filename_key = "file"
template_NNCS_NonLinearSys_func_key = "function"
template_NNCS_NonLinearSys_Cont_reachable_steps_key = "reachable-steps"


template_NNCS_NonLinearSys_param_keys = template_NNCS_param_keys.union({
    template_NNCS_NonLinearSys_func_key,
    template_NNCS_NonLinearSys_filename_key
})

template_NNCS_NonLinearSys_Discrete_param_keys = template_NNCS_NonLinearSys_param_keys
template_NNCS_NonLinearSys_Continuous_param_keys = template_NNCS_NonLinearSys_param_keys.union({template_NNCS_NonLinearSys_Cont_reachable_steps_key})


template_NN_param= {}
template_NN_param[template_NN_FFNN_key] = template_FFNN_param_keys
template_NN_param[template_NN_CNN_key] = template_CNN_param_keys
template_NN_param[template_NN_NNCS_ContinuousLinear_key] = template_NNCS_LinearSys_Cont_param_keys
template_NN_param[template_NN_NNCS_ContinuousNonLinear_key] = template_NNCS_NonLinearSys_Continuous_param_keys
template_NN_param[template_NN_NNCS_DiscreteLinear_key] = template_NNCS_LinearSys_Discrete_param_keys
template_NN_param[template_NN_NNCS_DiscreteNonLinear_key] = template_NNCS_NonLinearSys_Discrete_param_keys



template_parameter_file_name = "template_parameters.json"
output_directory_name = "/home/ubuntu/yogesh/nnv_data/inputs/"
upload_artifact_directory = "/home/ubuntu/yogesh/nnv_data/"

valid_meta_type_name_set = {
    "ExperimentIndex",
}
