from landsites import Land
from typing import List, Tuple, Union
from data_structures.heap import MaxHeap
from data_structures.bst import *

class Mode2Navigator:
    """
    Navigator for simulating a fair fight among multiple adventurer teams.
    """

    def __init__(self, n_teams: int) -> None:
        """
        Initialize the navigator with the number of teams.
        :param n_teams: Number of adventurer teams.
        """
        self.n_teams = n_teams
        self.sites = []

    def add_sites(self, sites: List[Land]) -> None:
        """
        Add land sites to the navigator.

        Parameters:
            sites (list[Land]): List of land sites, where each site is an instance of Land.

        Complexity:
            Best Case: O(N) - N is the number of elements in the sites list.
            Worst Case: O(N) - The same as the best case.
        """
        self.sites.extend(sites)

    def simulate_day(self, adventurer_size: int) -> List[Tuple[Union[Land, None], int]]:
        """
        Simulate a day of the game.

        Parameters:
            adventurer_size: an integer representing the number of adventurers for each team.

        Return:
            Returns a list of tuples where each tuple represents the choices made by each team. Each tuple contains:
                - An instance of Land or None if no site was chosen.
                - An integer representing the number of adventurers sent to the chosen site.

        Complexity:
            Best Case: O(n * log n + t)
            Worst Case: O(n * log n + t)

            where:
                - n is the number of land sites (length of self.sites)
                - t is the number of teams (self.n_teams)
        """
        choices = []

        heap = self.construct_score_data_structure(adventurer_size)

        for team in range(self.n_teams):
            if len(heap) == 0:
                choices.append((None, 0))
                continue

            best_score, best_site = heap.get_max()
            score, remaining_adventurers, gold_gained = self.compute_score(best_site, adventurer_size)
            if score == best_score:
                sent_adventurers = adventurer_size - remaining_adventurers
                choices.append((best_site, sent_adventurers))
                best_site.gold -= gold_gained
                best_site.guardians -= sent_adventurers
                
                new_score, _, _ = self.compute_score(best_site, adventurer_size)
                heap.add((new_score, best_site))

            else:
                choices.append((None, 0))

        return choices

    
    def compute_score(self, land: Land, adventurers: int) -> Tuple[float, int, float]:
        """
        Compute the score of a land site for a given number of adventurers.

        Parameters:
            land: an instance of Land.
            adventurers: an integer representing the number of adventurers coming to the land.

        Return:
            returns a tuple containing the score, remaining_adventurers, and gold_gained.

        Complexity:
            Best Case: O(1)
            Worst Case: O(1)
        """
        if land.guardians == 0:
            return 2.5 * adventurers, adventurers, 0

        ci = min(adventurers, land.guardians)
        gold_gained = min(ci * (land.gold / land.guardians), land.gold)
        remaining_adventurers = adventurers - ci
        score = 2.5 * remaining_adventurers + gold_gained
        return score, remaining_adventurers, gold_gained

    def construct_score_data_structure(self, adventurers: int):
        """
        Constructs a max-heap data structure containing the scores of land sites for a given number of adventurers.

        Parameters:
            adventurers: an integer representing the number of adventurers coming to explore the sites.

        Return:
            Returns a max-heap containing tuples where each tuple consists of the score and the corresponding site.

        Complexity:
            Best Case: O(n * log n)
            Worst Case: O(n * log n)

            where:
                - n is the number of land sites (length of self.sites)
        """
        heap = MaxHeap(len(self.sites))

        # Initialize the max-heap with land site scores
        for site in self.sites:
            score, _, _ = self.compute_score(site, adventurers)
            heap.add((score, site))

        return heap