# -*- coding: utf-8 -*-
"""
Created on Fri May  9 10:34:22 2025

@author: Huy Hung
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from interface import Interface
import time  # Import time module for timing
%matplotlib widget

class Interface:
    """
    Classe pour gérer l'interface graphique et l'animation de la simulation.
    Cette classe est conçue pour être compatible avec le code de simulation existant.
    """
    def __init__(self, positions_particules, vitesses_particules, temperatures, 
                 energies_cinetiques, energies_potentielles, energies_totales,
                 temperature_cible_tab, temps, taille_boite_simu, 
                 temperature_initiale, temperature_max):
        """
        Initialise l'interface graphique avec les données de simulation.
        
        Args:
            positions_particules (np.ndarray): Positions des particules à chaque pas de temps
            vitesses_particules (np.ndarray): Vitesses des particules à chaque pas de temps
            temperatures (np.ndarray): Températures à chaque pas de temps
            energies_cinetiques (np.ndarray): Énergies cinétiques à chaque pas de temps
            energies_potentielles (np.ndarray): Énergies potentielles à chaque pas de temps
            energies_totales (np.ndarray): Énergies totales à chaque pas de temps
            temperature_cible_tab (np.ndarray): Températures cibles à chaque pas de temps
            temps (np.ndarray): Tableau des temps
            taille_boite_simu (float): Taille de la boîte de simulation
            temperature_initiale (float): Température initiale
            temperature_max (float): Température maximale
        """
        self.positions_particules = positions_particules
        self.vitesses_particules = vitesses_particules
        self.temperatures = temperatures
        self.energies_cinetiques = energies_cinetiques
        self.energies_potentielles = energies_potentielles
        self.energies_totales = energies_totales
        self.temperature_cible_tab = temperature_cible_tab
        self.temps = temps
        self.taille_boite_simu = taille_boite_simu
        self.temperature_initiale = temperature_initiale
        self.temperature_max = temperature_max
        
        # Création de la figure et des sous-plots
        self.fig, self.ax = plt.subplots(1, 3, figsize=(18, 5))
        
        # Initialisation des sous-plots
        self._init_particules_plot()
        self._init_temperature_plot()
        self._init_energy_plot()
        
        # Création de l'animation
        self.ani = FuncAnimation(self.fig, self.update, frames=len(temps), 
                                interval=30, blit=True)
        
    def _init_particules_plot(self):
        """Initialise le sous-plot pour l'animation des particules."""
        ax_particules = self.ax[0]
        self.scatter_particules = ax_particules.scatter([], [], s=100, c='blue')
        self.texte_temps_ani = ax_particules.text(0.02, 0.95, '', 
                                                transform=ax_particules.transAxes)
        self.texte_temperature_cible_ani = ax_particules.text(0.02, 0.90, '', 
                                                            transform=ax_particules.transAxes)
        self.texte_temperature_initiale = ax_particules.text(0.02, 0.85, 
                                                           f'Température initiale: {self.temperature_initiale:.2f}', 
                                                           transform=ax_particules.transAxes)
        self.texte_temperature_max_atteinte = ax_particules.text(0.02, 0.80, 
                                                               f'Température max atteinte: {self.temperature_max:.2f}', 
                                                               transform=ax_particules.transAxes)
        ax_particules.set_xlim(0, self.taille_boite_simu)
        ax_particules.set_ylim(0, self.taille_boite_simu)
        ax_particules.set_aspect('equal')
        ax_particules.set_title("Mouvement des particules (Verlet + Lennard-Jones)")
        ax_particules.set_xlabel("x")
        ax_particules.set_ylabel("y")
        
    def _init_temperature_plot(self):
        """Initialise le sous-plot pour le graphique de température."""
        ax_temperature = self.ax[1]
        self.ligne_temperature_actuelle, = ax_temperature.plot([], [], 'r-', 
                                                             label='Température actuelle')
        self.ligne_temperature_cible, = ax_temperature.plot([], [], 'g--', 
                                                          label='Température cible (variable)')
        self.ligne_temp_init_hline = ax_temperature.axhline(y=self.temperature_initiale, 
                                                          color='b', linestyle='--', 
                                                          label='Température initiale')
        ax_temperature.set_xlabel("Temps")
        ax_temperature.set_ylabel("Température")
        ax_temperature.set_title("Évolution de la température en temps réel")
        ax_temperature.set_xlim(self.temps[0], self.temps[-1])
        ax_temperature.set_ylim(self.temperature_initiale * 0.9, self.temperature_max * 1.5)
        ax_temperature.legend()
        
    def _init_energy_plot(self):
        """Initialise le sous-plot pour le graphique des énergies."""
        ax_energie = self.ax[2]
        self.ligne_energie_cinetique, = ax_energie.plot([], [], 'b-', 
                                                      label='Énergie cinétique')
        self.ligne_energie_potentielle, = ax_energie.plot([], [], 'r-', 
                                                        label='Énergie potentielle')
        self.ligne_energie_totale, = ax_energie.plot([], [], 'g-', 
                                                   label='Énergie totale')
        ax_energie.set_xlabel("Temps")
        ax_energie.set_ylabel("Énergie")
        ax_energie.set_title("Évolution des énergies en temps réel")
        ax_energie.set_xlim(self.temps[0], self.temps[-1])
        ax_energie.legend()
        
    def update(self, frame):
        """Fonction de mise à jour pour l'animation."""
        # Mise à jour des positions des particules
        self.scatter_particules.set_offsets(self.positions_particules[frame])
        self.texte_temps_ani.set_text(f"Temps: {self.temps[frame]:.2f}")
        self.texte_temperature_cible_ani.set_text(f"T_cible: {self.temperature_cible_tab[frame]:.2f}")

        # Mise à jour des données de température
        self.ligne_temperature_actuelle.set_data(self.temps[:frame+1], 
                                               self.temperatures[:frame+1])
        self.ligne_temperature_cible.set_data(self.temps[:frame+1], 
                                            self.temperature_cible_tab[:frame+1])

        # Mise à jour des données d'énergie
        self.ligne_energie_cinetique.set_data(self.temps[:frame+1], 
                                            self.energies_cinetiques[:frame+1])
        self.ligne_energie_potentielle.set_data(self.temps[:frame+1], 
                                              self.energies_potentielles[:frame+1])
        self.ligne_energie_totale.set_data(self.temps[:frame+1], 
                                         self.energies_totales[:frame+1])

        # Mise à jour dynamique de l'axe y pour l'énergie
        max_energie = np.max(np.abs(np.array([
            self.energies_cinetiques[:frame+1],
            self.energies_potentielles[:frame+1],
            self.energies_totales[:frame+1]
        ])))
        if max_energie > self.ax[2].get_ylim()[1] or -max_energie < self.ax[2].get_ylim()[0]:
            self.ax[2].set_ylim(-max_energie * 1.1, max_energie * 1.1)
            self.ax[2].relim()
            self.ax[2].autoscale_view()

        return (self.scatter_particules, self.texte_temps_ani, 
                self.texte_temperature_cible_ani, self.ligne_temperature_actuelle,
                self.ligne_temperature_cible, self.ligne_energie_cinetique,
                self.ligne_energie_potentielle, self.ligne_energie_totale,
                self.ligne_temp_init_hline)
    
    def show(self):
        """Affiche l'animation."""
        plt.tight_layout()
        plt.show()

# Global timer start
global_start_time = time.time()

# Timer for constants and initialization
init_start_time = time.time()

# ----- Constantes -----
profondeur_puits_LJ = 1.0         # Profondeur du puits de potentiel de Lennard-Jones (epsilon)
distance_sigma_LJ = 1.0           # Distance à laquelle le potentiel de Lennard-Jones est nul (sigma)
rayon_coupure_LJ = 2.5 * distance_sigma_LJ   # Rayon de coupure pour le potentiel
taille_boite_simu = 10.0          # Taille de la boîte de simulation (carrée)
masse_particule = 1.0             # Masse des particules
constante_Boltzmann = 1.0         # Constante de Boltzmann (kB)
masse_thermostat = 5.0            # Masse du thermostat de Nose-Hoover (Q)
frequence_regulation_temperature = 1 # Fréquence de mise à jour du thermostat (en pas de temps)

# ----- Paramètres de simulation -----
rayon_coupure_LJ = 2.5 * distance_sigma_LJ   # Rayon de coupure pour le potentiel
taille_boite_simu = 10.0          # Taille de la boîte de simulation (carrée)
temperature_initiale = 0.7      # Température initiale (T_init)
temperature_max = 1.2          # (T_max)
nombre_particules = 36            # Nombre de particules (npart)
temps_debut = 0.0               # Temps initial (temps_initial)
temps_fin = 40.0               # Temps final (temps_final)
nombre_pas_temps = 3000         # Nombre d'itérations (nombre_iterations)
pas_temps = (temps_fin - temps_debut) / nombre_pas_temps   # Pas de temps (pas_de_temps)

# ----- Paramètres pour la liste de voisins -----
frequence_maj_voisins = 20
facteur_distance_voisinage = 3.0 * rayon_coupure_LJ
distance_voisinage_max = facteur_distance_voisinage * rayon_coupure_LJ
liste_voisins_particules = [[] for _ in range(nombre_particules)] # Initialisation vide (liste_voisins)


# ----- Création du profil de température cible en fonction du temps -----
temps_ajustement = np.linspace(temps_debut, temps_fin, nombre_pas_temps)
temperature_cible_tab = np.zeros_like(temps_ajustement)

phase1_fin = int(0.2 * nombre_pas_temps)
phase2_fin = int(0.4 * nombre_pas_temps)
phase3_fin = int(0.6 * nombre_pas_temps)
phase4_fin = nombre_pas_temps

temperature_cible_tab[:phase1_fin] = np.linspace(temperature_initiale, temperature_max, phase1_fin)
temperature_cible_tab[phase1_fin:phase2_fin] = temperature_max
temperature_cible_tab[phase2_fin:phase3_fin] = np.linspace(temperature_max, temperature_initiale, phase3_fin - phase2_fin)
temperature_cible_tab[phase3_fin:phase4_fin] = temperature_initiale

# Conversion de la température cible en énergie cinétique cible
energie_cinetique_cible_tab = nombre_particules * constante_Boltzmann * temperature_cible_tab



# ----- Initialisation des données -----
simulation_number = random.randint(1,20)
np.random.seed(simulation_number)

positions_particules = np.zeros((nombre_pas_temps, nombre_particules, 2))
vitesses_particules = np.zeros((nombre_pas_temps, nombre_particules, 2))
accelerations_particules = np.zeros((nombre_particules, 2))


# Conditions initiales : positions sur une grille carrée
cote_grille = int(np.sqrt(nombre_particules))
if cote_grille * cote_grille != nombre_particules:
    raise ValueError("Le nombre de particules doit être un carré parfait pour l'initialisation sur une grille carrée.")
espacement_grille = taille_boite_simu / cote_grille
x_grille, y_grille = np.meshgrid(np.arange(cote_grille) * espacement_grille + espacement_grille / 2, np.arange(cote_grille) * espacement_grille + espacement_grille / 2)
positions_particules[0] = np.column_stack((x_grille.ravel(), y_grille.ravel()))


# Initialisation des vitesses
vitesse_cible_init = np.sqrt(2 * constante_Boltzmann * temperature_initiale / masse_particule)
theta = 2 * np.pi * np.random.rand(nombre_particules)
vitesses_particules[0, :, 0] = vitesse_cible_init * np.cos(theta)
vitesses_particules[0, :, 1] = vitesse_cible_init * np.sin(theta)

# Suppression du mouvement du centre de masse initial
vitesse_centre_masse_initial = np.sum(vitesses_particules[0], axis=0) / nombre_particules
vitesses_particules[0] -= vitesse_centre_masse_initial


# Pré-calcul des constantes de Lennard-Jones
sigma_LJ_carre = distance_sigma_LJ**2
sigma_LJ_sixieme = sigma_LJ_carre**3
sigma_LJ_douzieme = sigma_LJ_sixieme**2
facteur_force_LJ = 24 * profondeur_puits_LJ
facteur_potentiel_LJ = 4 * profondeur_puits_LJ
rayon_coupure_carre_LJ = rayon_coupure_LJ**2

def mettre_a_jour_voisins(positions_actuelles, taille_boite, distance_voisinage):
    nombre_particules_local = len(positions_actuelles)
    voisins_local = [[] for _ in range(nombre_particules_local)]
    distance_voisinage_carre = distance_voisinage**2

    for i in range(nombre_particules_local):
        for j in range(i + 1, nombre_particules_local):
            dx = positions_actuelles[i] - positions_actuelles[j]
            dx = dx - taille_boite * np.round(dx / taille_boite)
            distance_carre = np.dot(dx, dx)
            if distance_carre < distance_voisinage_carre:
                voisins_local[i].append(j)
                voisins_local[j].append(i)
    return voisins_local

def forces_LJ_avec_voisins(positions, taille_boite, rayon_coupure_carre, profondeur_puits, sigma_carre, sigma_sixieme, facteur_force, liste_voisins):
    nombre_particules_local = len(positions)
    forces_lj = np.zeros_like(positions)

    for i in range(nombre_particules_local):
        for j_voisin in liste_voisins[i]:
            dx = positions[i] - positions[j_voisin]
            dx = dx - taille_boite * np.round(dx / taille_boite)
            distance_carre = np.dot(dx, dx)
            if 0 < distance_carre < rayon_coupure_carre:
                distance_carre_inv = 1.0 / distance_carre
                distance_sixieme_inv = sigma_sixieme * (distance_carre_inv)**3
                distance_douzieme_inv = distance_sixieme_inv**2
                force_scalaire = facteur_force * (2 * distance_douzieme_inv - distance_sixieme_inv) * np.sqrt(distance_carre_inv)
                force_ij = force_scalaire * dx
                forces_lj[i] += force_ij
                forces_lj[j_voisin] -= force_ij
    return forces_lj

def potentiel_LJ_avec_voisins(positions, taille_boite, rayon_coupure_carre, profondeur_puits, sigma_sixieme, sigma_douzieme, facteur_potentiel, liste_voisins):
    nombre_particules_local = len(positions)
    energie_potentielle_totale = 0.0
    for i in range(nombre_particules_local):
        for j_voisin in liste_voisins[i]:
            if j_voisin > i:
                dx = positions[i] - positions[j_voisin]
                dx = dx - taille_boite * np.round(dx / taille_boite)
                distance_carre = np.dot(dx, dx)
                if 0 < distance_carre < rayon_coupure_carre:
                    distance_sixieme_inv = sigma_sixieme * (1.0 / distance_carre)**3
                    distance_douzieme_inv = sigma_douzieme * (1.0 / distance_carre)**6
                    energie_potentielle_totale += facteur_potentiel * (distance_douzieme_inv - distance_sixieme_inv)
    return energie_potentielle_totale

# Initialisation des accélérations
liste_voisins_particules = mettre_a_jour_voisins(positions_particules[0], taille_boite_simu, distance_voisinage_max)
forces_initiales = forces_LJ_avec_voisins(positions_particules[0], taille_boite_simu, rayon_coupure_carre_LJ, profondeur_puits_LJ, sigma_LJ_carre, sigma_LJ_sixieme, facteur_force_LJ, liste_voisins_particules)
accelerations_particules = forces_initiales / masse_particule

# Tableaux pour stocker la température et l'énergie à chaque itération
temperatures = np.zeros(nombre_pas_temps)
energies_cinetiques = np.zeros(nombre_pas_temps)
energies_potentielles = np.zeros(nombre_pas_temps)
energies_totales = np.zeros(nombre_pas_temps)
temps = np.linspace(temps_debut, temps_fin, nombre_pas_temps)

# End of first timer
init_end_time = time.time()
init_time = init_end_time - init_start_time

# Timer for functions and initializations
func_start_time = time.time()

# ----- Intégration par l'algorithme de Verlet -----
# Initialize timing variables for if loops
voisins_time_total = 0
forces_time_total = 0
temp_reg_time_total = 0
voisins_count = 0
forces_count = 0
temp_reg_count = 0
# Initialize timing variables for forces and potential
forces_calc_time_total = 0
potential_calc_time_total = 0
forces_calc_count = 0
potential_calc_count = 0

# Initialize Nose-Hoover variables
zeta = 0.0  # Thermostat variable
zeta_point = 0.0  # Time derivative of thermostat variable

# ----- Parameters for Latent Heat Feature -----
temperature_transition = 1.0         # Temperature where phase change occurs
latent_heat_value = 2.0              # Latent heat absorbed/released per particle
transition_done = np.zeros(nombre_particules, dtype=bool)  # Track transitions


for i in range(nombre_pas_temps - 1):
    # Timer for neighbor list update
    if (i + 1) % frequence_maj_voisins == 0:
        voisins_start_time = time.time()
        liste_voisins_particules = mettre_a_jour_voisins(positions_particules[i], taille_boite_simu, distance_voisinage_max)
        voisins_end_time = time.time()
        voisins_time_total += (voisins_end_time - voisins_start_time)
        voisins_count += 1

    # Timer for force calculation
    forces_start_time = time.time()
    
    # Timer for forces calculation
    forces_calc_start_time = time.time()
    forces_lj = forces_LJ_avec_voisins(positions_particules[i], taille_boite_simu, rayon_coupure_carre_LJ, profondeur_puits_LJ, sigma_LJ_carre, sigma_LJ_sixieme, facteur_force_LJ, liste_voisins_particules)
    forces_calc_end_time = time.time()
    forces_calc_time_total += (forces_calc_end_time - forces_calc_start_time)
    forces_calc_count += 1
    
    # Timer for potential energy calculation
    potential_calc_start_time = time.time()
    energie_potentielle_instantannee = potentiel_LJ_avec_voisins(positions_particules[i], taille_boite_simu, rayon_coupure_carre_LJ, profondeur_puits_LJ, sigma_LJ_sixieme, sigma_LJ_douzieme, facteur_potentiel_LJ, liste_voisins_particules)
    potential_calc_end_time = time.time()
    potential_calc_time_total += (potential_calc_end_time - potential_calc_start_time)
    potential_calc_count += 1
    
    forces_end_time = time.time()
    forces_time_total += (forces_end_time - forces_start_time)
    forces_count += 1

    # Calcul de l'énergie cinétique instantanée
    energie_cinetique_instantannee = 0.5 * masse_particule * np.sum(vitesses_particules[i]**2)
    energies_cinetiques[i] = energie_cinetique_instantannee
    temperatures[i] = energie_cinetique_instantannee / (nombre_particules * constante_Boltzmann)

    # Nose-Hoover thermostat update
    # ----- Apply Latent Heat Absorption -----
    if (i + 1) % frequence_regulation_temperature == 0:
        for idx in range(nombre_particules):
            T_current = 0.5 * masse_particule * np.sum(vitesses_particules[i, idx]**2) / constante_Boltzmann
            if not transition_done[idx] and T_current >= temperature_transition:
                # Increase kinetic energy by latent heat (converted to velocity change)
                additional_energy = latent_heat_value
                current_velocity_sq = np.sum(vitesses_particules[i, idx]**2)
                current_energy = 0.5 * masse_particule * current_velocity_sq
                new_energy = current_energy + additional_energy
                scale_factor = np.sqrt(new_energy / current_energy)
                vitesses_particules[i, idx] *= scale_factor
                transition_done[idx] = True

        temp_reg_start_time = time.time()
        # Calculate current temperature
        T_current = temperatures[i]
        # Update zeta_point (thermostat equation of motion)
        zeta_point = (T_current - temperature_cible_tab[i]) / masse_thermostat
        # Update zeta
        zeta += zeta_point * pas_temps
        # Apply thermostat to velocities
        vitesses_particules[i] *= np.exp(-zeta * pas_temps)
        temp_reg_end_time = time.time()
        temp_reg_time_total += (temp_reg_end_time - temp_reg_start_time)
        temp_reg_count += 1

    # Mise à jour des accélérations en utilisant le principe de Newton avec le terme de Nose-Hoover
    accelerations_particules = (forces_lj - zeta * vitesses_particules[i]) / masse_particule

    # Mise à jour des vitesses (Verlet velocity)
    vitesses_particules[i+1] = vitesses_particules[i] + pas_temps * accelerations_particules

    # Mise à jour des positions (Verlet velocity)
    positions_particules[i+1] = positions_particules[i] + pas_temps * vitesses_particules[i+1]

    # Conditions périodiques : repliement dans la boîte
    positions_particules[i+1] %= taille_boite_simu

    # Recalcul de la liste des voisins
    if (i + 1) % frequence_maj_voisins == 0:
        liste_voisins_particules = mettre_a_jour_voisins(positions_particules[i+1], taille_boite_simu, distance_voisinage_max)
    
    # ----- Calcul de l'énergie -----
    energie_cinetique_instantannee_next = 0.5 * masse_particule * np.sum(vitesses_particules[i+1]**2)
    energie_totale_instantanee = energie_cinetique_instantannee_next + energie_potentielle_instantannee

    temperatures[i+1] = energie_cinetique_instantannee_next / (nombre_particules * constante_Boltzmann)
    energies_cinetiques[i+1] = energie_cinetique_instantannee_next
    energies_potentielles[i+1] = energie_potentielle_instantannee
    energies_totales[i+1] = energie_totale_instantanee

# End of second timer
func_end_time = time.time()
func_time = func_end_time - func_start_time


# Timer for interface creation and display
interface_start_time = time.time()

# Create and show interface
interface = Interface(
    positions_particules=positions_particules,
    vitesses_particules=vitesses_particules,
    temperatures=temperatures,
    energies_cinetiques=energies_cinetiques,
    energies_potentielles=energies_potentielles,
    energies_totales=energies_totales,
    temperature_cible_tab=temperature_cible_tab,
    temps=temps,
    taille_boite_simu=taille_boite_simu,
    temperature_initiale=temperature_initiale,
    temperature_max=temperature_max
)

# End of interface timer
interface_end_time = time.time()
interface_time = interface_end_time - interface_start_time

# Global timer end
global_end_time = time.time()
global_time = global_end_time - global_start_time

# Print timing results
print("\n=== Timing Results ===")
print(f"Initialization time (constants and setup): {init_time:.6f} seconds")
print(f"Functions and initializations time: {func_time:.6f} seconds")
print(f"\n=== Verlet Integration Loop Timing ===")
print(f"Neighbor list updates (total time): {voisins_time_total:.6f} seconds")
print(f"Neighbor list updates (average time): {voisins_time_total/voisins_count:.6f} seconds")
print(f"\nForce calculations section:")
print(f"  Total section time: {forces_time_total:.6f} seconds")
print(f"  Forces calculation (total time): {forces_calc_time_total:.6f} seconds")
print(f"  Forces calculation (average time): {forces_calc_time_total/forces_calc_count:.6f} seconds")
print(f"  Potential energy calculation (total time): {potential_calc_time_total:.6f} seconds")
print(f"  Potential energy calculation (average time): {potential_calc_time_total/potential_calc_count:.6f} seconds")
print(f"\nTemperature regulation (total time): {temp_reg_time_total:.6f} seconds")
print(f"Temperature regulation (average time): {temp_reg_time_total/temp_reg_count:.6f} seconds")
print(f"\nInterface creation and display time: {interface_time:.6f} seconds")
print(f"Total execution time: {global_time:.6f} seconds")

interface.show()