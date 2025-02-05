import random
from config.config import emodji as emodji_list

def generate_emojis() -> str:
    num_emodji_start = random.randint(0, 3)
    num_emodji_end = random.randint(0, 3)

    selected_emodji_start = random.sample(emodji_list, num_emodji_start) if num_emodji_start > 0 else []
    selected_emodji_end = []

    if num_emodji_end > 0:
        remaining_emodji = list(set(emodji_list) - set(selected_emodji_start))
        selected_emodji_end = random.sample(remaining_emodji, min(num_emodji_end, len(remaining_emodji)))

    return selected_emodji_start, selected_emodji_end


