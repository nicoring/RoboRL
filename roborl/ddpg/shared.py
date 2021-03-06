import argparse

import gym
import roboschool

from ddpg import DDPG
from models import Actor, Critic, SharedControllerActor


def run(args):
    env = gym.make(args.env)
    n_states = env.observation_space.shape[0]
    n_actions = env.action_space.shape[0]
    controller_conf = {
        'leg': {
            'actions': 2,
            'hidden': 40
        }
    }
    controller_list = ['leg', 'leg', 'leg', 'leg']
    actor = SharedControllerActor(n_states, controller_conf, controller_list, args.actor_hidden, args.batchnorm)
    critic = Critic(n_states, n_actions, args.critic_hidden, args.batchnorm)
    try:
        ddpg = DDPG(env, actor, critic, args.replay_memory, args.batch_size, args.gamma,
                    args.tau, args.lr_actor, args.lr_critic, args.decay_critic,
                    render=args.render, evaluate=args.evaluate, save_path=args.save_path,
                    save_every=args.save_every)
        rewards, losses = ddpg.train(args.steps)
    finally:
        env.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyTorch DDPG implementation')
    # parser.add_argument('--env', help='OpenAI Gym env name', default='RoboschoolInvertedPendulum-v1')
    parser.add_argument('--critic_hidden', type=int, default=100)
    parser.add_argument('--actor_hidden', type=int, default=100)
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--steps', type=int, default=10000)
    parser.add_argument('--replay_memory', type=int, default=100000)
    parser.add_argument('--gamma', type=float, default=0.99)
    parser.add_argument('--tau', type=float, default=0.001)
    parser.add_argument('--lr_actor', type=float, default=1e-3)
    parser.add_argument('--lr_critic', type=float, default=1e-4)
    parser.add_argument('--decay_critic', type=float, default=1e-2)
    parser.add_argument('--render', default=False, dest='render', action='store_true')
    parser.add_argument('--evaluate', type=int, default=10)
    parser.add_argument('--save_path', default=None)
    parser.add_argument('--save_every', type=int, default=10)
    parser.add_argument('--batchnorm', default=False, dest='batchnorm', action='store_true')

    args = parser.parse_args()
    args.env = 'RoboschoolAnt-v1'
    run(args)
