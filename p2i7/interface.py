import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

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