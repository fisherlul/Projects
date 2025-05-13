# ----- Libraires ------
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# ----- Constantes -----
epsilon = 1.0  # Profondeur du puits de potentiel de Lennard-Jones
sigma = 1.0    # Distance à laquelle le potentiel de Lennard-Jones est nul
rayon_coupure = 2.5 * sigma  # Rayon de coupure pour le potentiel
box_size = 10.0  # Taille de la boîte de simulation (carrée)
mass = 1.0     # Masse des particules
kbT_cible_init = 0.1 # Température cible initiale
kB = 1.0       # Constante de Boltzmann (fixée à 1.0 pour simplifier)

# ----- Paramètres de simulation -----
npart = 49    # Nombre de particules
tinit = 0      # Temps initial
tfin = 100     # Temps final
Niter = 2000   # Nombre d'itérations
dt = (tfin - tinit) / Niter  # Pas de temps
frequence_ajustement_T = 50 # Fréquence (en nombre de pas de temps) à laquelle ajuster la température
temperature_cible = 0.5 # Température cible que tu peux modifier

# ----- Initialisation des données -----
np.random.seed(1) # Pour la reproductibilité des résultats

# Tableaux pour stocker les positions et les vitesses à chaque itération
positions = np.zeros((Niter, npart, 2)) # positions[temps, particule, coordonnée (x, y)]
velocities = np.zeros((Niter, npart, 2)) # vitesses[temps, particule, coordonnée (vx, vy)]

# Conditions initiales : positions sur une grille carrée
side = int(np.sqrt(npart))
if side * side != npart:
    raise ValueError("Le nombre de particules doit être un carré parfait pour l'initialisation sur une grille carrée.")
spacing = box_size / side
x, y = np.meshgrid(np.arange(side) * spacing + spacing / 2, np.arange(side) * spacing + spacing / 2) # Centrage des particules dans les cellules
positions[0] = np.column_stack((x.ravel(), y.ravel()))

# Initialisation des vitesses avec une norme correspondant à la température cible initiale et une direction aléatoire
vitesse_cible_init = np.sqrt(2 * kB * kbT_cible_init / mass)
theta = 2 * np.pi * np.random.rand(npart)
velocities[0, :, 0] = vitesse_cible_init * np.cos(theta)
velocities[0, :, 1] = vitesse_cible_init * np.sin(theta)

# Tableaux pour stocker la température et le temps à chaque itération
temperatures = np.zeros(Niter)
times = np.linspace(tinit, tfin, Niter)

# ----- Fonction de force de Lennard-Jones -----
def forces_LJ(pos, box_size, rayon_coupure, epsilon, sigma):
    """
    Calcul des forces de Lennard-Jones entre paires de particules avec conditions aux limites périodiques.

    Args:
        pos (np.ndarray): Tableau NumPy de taille (npart, 2) contenant les positions (x, y) de chaque particule.
        box_size (float): Taille de la boîte de simulation (carrée).
        rayon_coupure (float): Distance maximale pour laquelle les forces sont calculées.
        epsilon (float): Profondeur du puits de potentiel de Lennard-Jones.
        sigma (float): Distance à laquelle le potentiel de Lennard-Jones est nul.

    Returns:
        np.ndarray: Tableau NumPy de taille (npart, 2) contenant les forces (Fx, Fy) sur chaque particule.
    """
    npart = len(pos)
    F = np.zeros_like(pos)

    for i in range(npart):
        for j in range(i + 1, npart):
            # Vecteur de distance entre les particules i et j
            dx = pos[i] - pos[j] # Calcul vectoriel de la distance sur x et y

            # Application des conditions aux limites périodiques (image minimale)
            dx = dx - box_size * np.round(dx / box_size)

            # Carré de la distance entre les particules
            r2 = np.dot(dx, dx)

            # Vérification si la distance est dans le rayon de coupure (et non nulle)
            if 0 < r2 < rayon_coupure**2:
                # Calcul des termes pour le potentiel de Lennard-Jones
                r6_inv = (sigma*2 / r2)*3
                r12_inv = r6_inv**2

                # Magnitude de la force de Lennard-Jones
                F_scalar = 24 * epsilon * (2 * r12_inv - r6_inv) / np.sqrt(r2)

                # Vecteur de force sur la particule i due à la particule j
                fij = F_scalar * dx

                # Application de la troisième loi de Newton (forces opposées et égales)
                F[i] += fij
                F[j] -= fij

    return F


# ----- Système différentiel : retourne vitesse et accélération -----
def F(pos, vit, box_size, rayon_coupure, epsilon, sigma, mass):
    """
    Calcule le vecteur d'état dérivé (vitesse et accélération) pour l'intégration temporelle.

    Args:
        pos (np.ndarray): Tableau NumPy de taille (npart, 2) contenant les positions.
        vit (np.ndarray): Tableau NumPy de taille (npart, 2) contenant les vitesses.
        box_size (float): Taille de la boîte de simulation.
        rayon_coupure (float): Rayon de coupure du potentiel.
        epsilon (float): Profondeur du puits de potentiel.
        sigma (float): Distance caractéristique du potentiel.
        mass (float): Masse des particules.

    Returns:
        np.ndarray: Tableau NumPy de taille (2, npart, 2) contenant les vitesses et les accélérations.
                     Le premier élément est le tableau des vitesses, le second est le tableau des accélérations.
    """
    acc = forces_LJ(pos, box_size, rayon_coupure, epsilon, sigma) / mass
    return np.array([vit, acc])

# Ajout de la chaleur latente 
T_melt = 0.5                      # Température de fusion
latent_heat_energy = 2.0         # Chaleur latente par particule
latent_energy_accum = 0.0        # Énergie accumulée pendant le changement de phase
melting_done = False             # Statut du changement de phase

# ----- Intégration par Runge-Kutta 4ème ordre -----
for i in range(Niter - 1):
    K1 = F(positions[i], velocities[i], box_size, rayon_coupure, epsilon, sigma, mass)
    K2 = F(positions[i] + dt/2 * K1[0], velocities[i] + dt/2 * K1[1], box_size, rayon_coupure, epsilon, sigma, mass)
    K3 = F(positions[i] + dt/2 * K2[0], velocities[i] + dt/2 * K2[1], box_size, rayon_coupure, epsilon, sigma, mass)
    K4 = F(positions[i] + dt * K3[0], velocities[i] + dt * K3[1], box_size, rayon_coupure, epsilon, sigma, mass)

    positions[i+1] = positions[i] + dt/6 * (K1[0] + 2*K2[0] + 2*K3[0] + K4[0])
    velocities[i+1] = velocities[i] + dt/6 * (K1[1] + 2*K2[1] + 2*K3[1] + K4[1])

    positions[i+1] = positions[i+1] % box_size

    kinetic_energy = 0.5 * mass * np.sum(velocities[i+1]**2)
    current_temperature = kinetic_energy / (npart * kB)
    temperatures[i+1] = current_temperature

    if (i + 1) % frequence_ajustement_T == 0:
        if not melting_done:
            if current_temperature < T_melt:
                facteur_echelle = np.sqrt(temperature_cible / current_temperature)
                velocities[i+1] *= facteur_echelle
            elif current_temperature >= T_melt:
                # Stocker l'énergie sous forme de chaleur latente sans augmenter KE
                latent_energy_accum += (temperature_cible - T_melt) * npart * kB
                temperatures[i+1] = T_melt
                velocities[i+1] *= np.sqrt(T_melt / current_temperature)  # maintien de la temp à T_melt
                if latent_energy_accum >= latent_heat_energy * npart:
                    melting_done = True
        else:
            facteur_echelle = np.sqrt(temperature_cible / current_temperature)
            velocities[i+1] *= facteur_echelle


# ----- Animation avec matplotlib -----
fig, ax = plt.subplots(1, 2, figsize=(12, 5)) # Création de deux sous-plots

# Sous-plot pour l'animation des particules
ax_particles = ax[0]
sc = ax_particles.scatter([], [], s=100, c='blue')
time_text = ax_particles.text(0.02, 0.95, '', transform=ax_particles.transAxes)
temp_cible_text = ax_particles.text(0.02, 0.90, f'T_cible: {temperature_cible:.2f}', transform=ax_particles.transAxes)
ax_particles.set_xlim(0, box_size)
ax_particles.set_ylim(0, box_size)
ax_particles.set_aspect('equal')
ax_particles.set_title("Mouvement des particules (RK4 + Lennard-Jones)")
ax_particles.set_xlabel("x")
ax_particles.set_ylabel("y")

# Sous-plot pour le graphique de température en temps réel
ax_temp = ax[1]
line_temp, = ax_temp.plot([], [], 'r-', label='Température actuelle')
ax_temp.axhline(y=temperature_cible, color='g', linestyle='--', label='Température cible')
ax_temp.set_xlabel("Temps")
ax_temp.set_ylabel("Température")
ax_temp.set_title("Évolution de la température en temps réel")
ax_temp.set_xlim(tinit, tfin)
ax_temp.set_ylim(0, np.max(temperatures) * 1.1 if np.max(temperatures) > 0 else 1.0) # Ajustement dynamique de l'axe y
ax_temp.legend()

# Fonction de mise à jour pour l'animation
def update(frame):
    sc.set_offsets(positions[frame])
    time_text.set_text(f"Temps: {times[frame]:.2f}")
    line_temp.set_data(times[:frame+1], temperatures[:frame+1])
    # Mise à jour dynamique de l'axe y de la température
    if np.max(temperatures[:frame+1]) > ax_temp.get_ylim()[1]:
        ax_temp.set_ylim(0, np.max(temperatures[:frame+1]) * 1.1)
    return sc, time_text, line_temp

# Création de l'animation
ani = FuncAnimation(fig, update, frames=Niter, interval=30, blit=True)
plt.tight_layout()
plt.show()