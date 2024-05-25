from landsites import Land


from typing import List, Tuple

class Land:
    def __init__(self, name: str, gold: float, guardians: int) -> None:
        self.name = name
        self.gold = gold
        self.guardians = guardians

class Mode1Navigator:
    """
    Navigator for selecting the optimal land sites for adventurers to invade.
    """
    
    def __init__(self, sites: List[Land], adventurers: int) -> None:
        """
        Initialize the navigator with the list of land sites and the number of adventurers.

        :param sites: List of Land objects.
        :param adventurers: Total number of adventurers available.
        """
        self.sites = sites
        self.adventurers = adventurers
        # Precompute the ratio of gold to guardians for each site for quick selection
        self.ratios = [(site.gold / site.guardians if site.guardians != 0 else float('inf'), site) for site in sites]
        # Sort sites based on the gold-to-guardian ratio in descending order
        self.ratios.sort(key=lambda x: -x[0])
    
    def select_sites(self) -> List[Tuple[Land, int]]:
        """
        Select the land sites to attack to maximize the reward.

        :return: List of tuples, where each tuple contains a Land object and the number of adventurers to send.
        """
        result = []
        remaining_adventurers = self.adventurers
        
        for ratio, site in self.ratios:
            if remaining_adventurers == 0:
                break
            if site.gold > 0 and site.guardians > 0:
                # Calculate the optimal number of adventurers to send
                ci = min(remaining_adventurers, site.guardians)
                result.append((site, ci))
                remaining_adventurers -= ci
        
        return result

    def select_sites_from_adventure_numbers(self, adventure_numbers: List[int]) -> List[float]:
        """
        Calculate the maximum amount of reward for different numbers of adventurers.

        :param adventure_numbers: List of numbers of adventurers for each configuration.
        :return: List of maximum rewards for each configuration.
        """
        rewards = []
        
        for num_adventurers in adventure_numbers:
            total_reward = 0.0
            remaining_adventurers = num_adventurers
            
            for ratio, site in self.ratios:
                if remaining_adventurers == 0:
                    break
                if site.gold > 0 and site.guardians > 0:
                    ci = min(remaining_adventurers, site.guardians)
                    reward = min(ci * (site.gold / site.guardians), site.gold)
                    total_reward += reward
                    remaining_adventurers -= ci
            
            rewards.append(total_reward)
        
        return rewards

    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        Update the state of a land site.

        :param land: Land object to be updated.
        :param new_reward: New amount of reward (gold) for the land site.
        :param new_guardians: New number of guardians for the land site.
        """
        land.gold = new_reward
        land.guardians = new_guardians
        # Update the precomputed ratios
        self.ratios = [(site.gold / site.guardians if site.guardians != 0 else float('inf'), site) for site in self.sites]
        self.ratios.sort(key=lambda x: -x[0])


