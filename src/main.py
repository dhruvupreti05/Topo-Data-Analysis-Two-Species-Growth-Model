
from msep import MultiSpeciesExclusionProcess

if __name__ == "__main__":
    dimension = 3
    density = [1/3,1/3,1/3]

    rates = {(0,1) : 2.0, (1,0) : 1.0, (0,2) : 2.0, (2,0) : 1.0, (1,2) : 1.5, (2,1) : 1.5}
    length = 90

    asym_diffusion_2d = MultiSpeciesExclusionProcess(dimension=dimension, density=density, rates=rates, length=length)
    asym_diffusion_2d.simulate()
    asym_diffusion_2d.plot_path_3d()

