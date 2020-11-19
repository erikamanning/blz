import string


class PolicyAreas():

    def __init__(self):

        self.policy_areas = self.read_dict("policy_areas.txt")

    def read_dict(self,lst_path):

        pas_file = open(lst_path)
        policy_areas = [p.strip() for p in pas_file]
        pas_file.close()
        return policy_areas

