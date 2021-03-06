from agents import EigenOCAgent
from agents import LinearSFAgent
from agents import EigenOCAgentDyn
from agents import DynSRAgent
from env_tools import GridWorld
import functools
from networks import EignOCNetwork
from networks import LinearSFNetwork
from networks import DynSRNetwork
from networks import EignOCMontezumaNetwork

def default():
  num_agents = 8
  use_gpu = False

  weight_summaries = dict(
    all=r'.*')
  input_size = (13, 13)
  history_size = 3
  network_optimizer = 'AdamOptimizer'
  lr = 0.0001
  discount = 0.99
  sf_coef = 1
  aux_coef = 1
  entropy_coef = 0.01
  critic_coef = 1
  eigen_critic_coef = 1
  target_update_iter_aux = 1
  target_update_iter_sf = 30
  target_update_iter_option = 30

  goal_locations = [(11, 7), (5, 2), (1, 10), (2, 2), (6, 2)]
  move_goal_nb_of_ep = 1000

  env = functools.partial(
    GridWorld, goal_locations, "./mdps/4rooms.mdp")

  max_update_freq = 30
  min_update_freq = 5
  aux_update_freq = 1

  steps = -1  # 10M
  episodes = 1e6  # 1M

  final_random_option_prob = 0.1
  final_random_action_prob = 0.01

  nb_test_ep = 100
  max_length = 1000

  gradient_clip_norm_value = 40
  clip_option_grad_by_value = False
  clip_by_value = 5

  steps_summary_interval = 1000
  episode_summary_interval = 10
  steps_checkpoint_interval = 1000
  episode_checkpoint_interval = 10
  episode_eval_interval = 10

  return locals()

def linear_sf():
  locals().update(default())
  dif_agent = LinearSFAgent
  num_agents = 8
  nb_options = 4
  network = LinearSFNetwork

  input_size = (13, 13)
  history_size = 3
  conv_layers = (5, 2, 32),
  fc_layers = 128,
  sf_layers = 128, 128
  lr = 1e-3
  sf_lr = 1e-3
  discount = 0.985
  entropy_coef = 1e-4 #0.01
  critic_coef = 0.5
  sf_coef = 1
  instant_r_coef = 1
  option_entropy_coef = 0.01
  auto_coef = 1

  steps = -1  # 1M
  explore_steps = 1e5
  delib_cost = 0
  margin_cost = 0
  gradient_clip_value = 40
  summary_interval = 10
  checkpoint_interval = 1
  eval_interval = 1
  policy_steps = 1e3
  sf_transition_matrix_steps = 300#e3
  sf_transition_options_steps = 400#e3
  sf_transition_matrix_size = 1e3

  return locals()

def dynamic_SR():
  locals().update(default())
  dif_agent = DynSRAgent
  num_agents = 8
  network = DynSRNetwork

  input_size = (13, 13)
  history_size = 3
  fc_layers = 128,
  sf_layers = 128,
  aux_fc_layers = 507,
  lr = 1e-3
  discount = 0.985

  batch_size = 16
  memory_size = 500000
  observation_steps = 1000
  steps = 1e6   # 1M
  training_steps = 5e5
  summary_interval = 10
  checkpoint_interval = 10
  max_length = 1e20

  return locals()

def oc():
  locals().update(default())
  nb_options = 4
  dif_agent = EigenOCAgent
  eigen = False
  network = EignOCNetwork

  fc_layers = 128,
  sf_layers = 128,
  aux_fc_layers = 507,

  batch_size = 32
  memory_size = 100000
  observation_steps = 16*4

  steps = -1  # 1M
  episodes = 1e6  # 1M
  eigen_exploration_steps = 16*4
  max_length = 1000
  max_length_eval = 1000
  include_primitive_options = True
  sr_matrix_size = 169
  sr_matrix = "static"
  goal_locations = [(11, 7), (5, 2), (1, 10), (2, 2), (6, 2)]
  move_goal_nb_of_ep = 1000

  return locals()

def eigenoc():
  locals().update(default())
  dif_agent = EigenOCAgent
  nb_options = 4
  eigen = True
  network = EignOCNetwork

  fc_layers = 128,
  sf_layers = 128,
  aux_fc_layers = 507,

  batch_size = 32
  memory_size = 100000
  observation_steps = 16*4

  alpha_r = 0.75
  eigen_exploration_steps = 16*4
  max_length = 1000
  max_length_eval = 1000
  first_eigenoption = 1
  include_primitive_options = True
  sr_matrix_size = 169
  sr_matrix = "static"
  goal_locations = [(11, 7), (5, 2), (1, 10), (2, 2), (6, 2)]
  move_goal_nb_of_ep = 1000
  return locals()

def eigenoc_dyn():
  locals().update(eigenoc())
  dif_agent = EigenOCAgentDyn
  sf_matrix_size = 5000
  sr_matrix = "dynamic"
  goal_locations = [(11, 7), (5, 2), (1, 10), (2, 2), (6, 2)]
  move_goal_nb_of_ep = 1000
  return locals()

def oc_dyn():
  locals().update(oc())
  dif_agent = EigenOCAgentDyn
  sr_matrix = None
  goal_locations = [(11, 7), (5, 2), (1, 10), (2, 2), (6, 2)]
  move_goal_nb_of_ep = 1000
  return locals()

def eigenoc_montezuma():
  locals().update(default())
  dif_agent = EigenOCAgentDyn
  eigen = True
  network = EignOCMontezumaNetwork

  input_size = (84, 84)
  history_size = 4
  channel_size = 1
  conv_layers = (6, 2, 0, 64), (6, 2, 2, 64), (6, 2, 2, 64),
  upconv_layers = (6, 2, 2, 64), (6, 2, 2, 64), (6, 2, 0, 1)
  fc_layers = 1024, 2048
  sf_layers = 2048, 1024, 2048
  aux_fc_layers = 2048, 1024, 10*10*64
  aux_upconv_reshape = (10, 10, 64)

  env = "MontezumaRevenge-v0"
  batch_size = 32
  memory_size = 500000
  observation_steps = 16*4
  alpha_r = 0.75
  steps = -1  # 10M
  eigen_exploration_steps = 16*4
  episode_eval_interval = 100
  max_length_eval = 1000
  nb_test_ep = 1
  first_eigenoption = 1
  include_primitive_options = True
  sf_matrix_size = 50000
  sr_matrix = "dynamic"

  return locals()


