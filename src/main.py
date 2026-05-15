
from msep import MultiSpeciesExclusionProcess

if __name__ == "__main__":

    
    dimension = 3
    density = [1/3,1/3,1/3]

    rates = {(0,1) : 2.0, (1,0) : 1.0, (0,2) : 2.0, (2,0) : 1.0, (1,2) : 1.5, (2,1) : 1.5}
    length = 90

    asym_diffusion_2d = MultiSpeciesExclusionProcess(dimension=dimension, density=density, rates=rates, length=length)
    _ = asym_diffusion_2d.simulate()
    asym_diffusion_2d.plot_path_2d()
    

    dimension = 4
    density = [1/4, 1/4, 1/4, 1/4]
    rates = { (0, 1): 1.6, (1, 0): 2.4, (0, 2): 2.3, (2, 0): 1.7, (0, 3): 1.8, (3, 0): 2.2, (1, 2): 2.7, (2, 1): 1.3, (1, 3): 2.2, (3, 1): 1.8, (2, 3): 1.5, (3, 2): 2.5, }
    length = 120 
    asym_diffusion_3d = MultiSpeciesExclusionProcess(dimension=dimension, density=density, rates=rates, length=length)
    _ = asym_diffusion_3d.simulate()
    asym_diffusion_3d.plot_path_3d()
