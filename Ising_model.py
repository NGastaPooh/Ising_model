import numpy as np
import numpy.typing as npt
import matplotlib.pylab as plt
import matplotlib.animation as animation
import matplotlib.image as image
from sys import exit


# Primary system parameters
N = 256  # system size NxN
MC_steps = 10 ** 6  # number of Monte-Carlo steps

# read user specified primary parameters
T = float(input("Specify a positive value for temperature T"
                " (hints: <= 1.0 is somewhat cold, >=5.0 is somewhat hot, "
                "2.269 - critical, 1.69 - Jetstream Sam):\n"))
if T <= 0:
    exit("Temperature must be a positive number")
initial_system_config = int(input("Chose which initial system configuration to generate:"
                                  "type 1 for COLD or 2 for WARM:\n"))
if initial_system_config not in [1, 2]:
    exit("must chose one of the proposed configurations")
print("Simulating ...")

# Secondary system parameters
beta = 1.0 / T  # thermodynamics' betta
p = np.array([0., 0.])  # initializes probability array
p[0] = np.exp(-4.0 * beta)  # for a 2D square system, there's only 2 relevant probabilities, p[0] and p[1],
p[1] = np.exp(-8.0 * beta)  # at a given temperature T

# Animation parameters
number_of_frames = 500

# Initializing pseudo random number generator
rng = np.random.default_rng()


def energy_change(system: npt.NDArray, i: int, j: int) -> npt.NDArray:
    """Energy change due to a single spin flip located at (i, j) coordinates"""
    return 2 * system[i][j] * (system[(N + i - 1) % N][j]
                               + system[(i + 1) % N][j]
                               + system[i][(N + j - 1) % N]
                               + system[i][(j + 1) % N])


def metropolis(system: npt.NDArray) -> npt.NDArray:
    """A single system update according to Metropolis Monte-Carlo algorythm"""
    i0 = rng.integers(0, N)  # choose a random spin at (i0, j0) position
    j0 = rng.integers(0, N)
    delta_energy = energy_change(system, i0, j0)
    if delta_energy <= 0:
        system[i0][j0] = -system[i0][j0]  # if energy gets lower or stays the same, flip the spin
    else:
        # all possible values of energy change, 4 and 8, can be directly related to a corresponding
        # index in the probability array p
        if rng.random() < p[int(delta_energy / 4 - 1)]:
            system[i0][j0] = -system[i0][j0]  # if energy increases, flip the spin according to Boltzmann statistics
    return system


# A secret function
def samopolis(system: npt.NDArray, sam: npt.NDArray) -> npt.NDArray:
    """There will be bloodshed"""
    i0 = rng.integers(0, N)
    j0 = rng.integers(0, N)
    if system[i0][j0] != sam[i0][j0]:
        system[i0][j0] = -system[i0][j0]
    else:
        if rng.random() < p[0]:
            system[i0][j0] = -system[i0][j0]
    return system


def main():
    # initialize the system according to the user's input
    if initial_system_config == 1:
        system = -2 * np.ones((N, N)) + 1  # generates initial "COLD" configuration
    else:
        system = 2 * rng.integers(0, 2, (N, N)) - 1  # generates initial "WARM" configuration

    animation_frames = np.zeros((number_of_frames, N, N))  # will track current system state to use for the animation
    animation_frames[0, :, :] = system  # 1st animation frame is the initial system configuration

    # every "steps_between_frames" another frame will be recorded
    steps_between_frames = int(MC_steps / number_of_frames)

    if T != 1.69:  # just a regular MC run
        # Run a simulation for MC_steps according to Metropolis algorythm
        # Note: MC_steps = number_of_frames * steps_between_frames
        for i in range(number_of_frames):
            for j in range(steps_between_frames):
                system = metropolis(system)
            animation_frames[i, :, :] = system
    else:  # secret Jetstream Sam run
        img_two_colors = np.loadtxt('sam.txt', dtype='int', delimiter=',')
        for i in range(number_of_frames):
            for j in range(steps_between_frames):
                system = samopolis(system, img_two_colors)
            animation_frames[i, :, :] = system

    # Initialize matplotlib figure
    fig = plt.figure()
    ax = plt.gca()
    # Visualize the 1st frame, set up color scheme
    picture = ax.imshow(animation_frames[0, :, :], cmap='Greys', vmin=-1, vmax=1)
    # remove ticks and labels
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    # a function that generates n images of the system; needed for the animation
    def frames_scrolling_function(n: int) -> image.AxesImage:
        picture.set_data(animation_frames[n, :, :])
        return picture

    # animate system evolution with 30 ms delay between frames
    animate = animation.FuncAnimation(fig, frames_scrolling_function, frames=number_of_frames,
                                      interval=30, blit=False, repeat=False)
    plt.show()


if __name__ == "__main__":
    main()
