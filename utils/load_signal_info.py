import asammdf
import numpy as np
import yaml
from tqdm import tqdm


def extract_signal_info_and_save(mf4_filepath: str, 
                                 yaml_filepath: str):
    NUMERIC_SIGNAL_TYPE = "numeric"
    TEXT_SIGNAL_TYPE = "text"

    # Extract signal names, types, and possible values 
    numeric_signals_info = {}
    text_signals_info = {}

    # Load mf4 file
    mdf = asammdf.MDF(mf4_filepath)
    mdf.configure(raise_on_multiple_occurrences=False)

    channels_list = list(set([channel['name'] for group in mdf.groups for channel in group['channels']]))

    # Preallocate memory
    numeric_signals_info = {}
    text_signals_info = {}

    # Looping through each groups
    for signal_name in tqdm(channels_list):            
        signal_samples = mdf.get(signal_name).samples

        # Extract type from signal
        signal_type = NUMERIC_SIGNAL_TYPE if np.issubdtype(signal_samples.dtype, np.number) else TEXT_SIGNAL_TYPE

        # Unit "Not available" if it does not have
        unit = mdf.get(signal_name).unit

        # Replace "off" unit
        if "_per_" in unit:
            unit = unit.replace("_per_", "/")
        if unit=="C" or unit=="DegreeC":
            unit = "°C"
            
        # If numeric then
        if signal_type == NUMERIC_SIGNAL_TYPE:
            # Filter NaN values
            signal_samples = signal_samples[~np.isnan(signal_samples)]

            # Possible values
            if len(signal_samples) > 2:
                min_val = int(np.ceil(np.min(signal_samples)))
                max_val = int(np.ceil(np.max(signal_samples)))
                possible_values = [min_val, max_val]

            else:
                possible_values = [np.nan, np.nan]


            # Append to numeric signal info dict
            numeric_signals_info[signal_name] = {"possible_values": possible_values, "unit":unit}
        elif signal_type == TEXT_SIGNAL_TYPE:
            # Possible values
            possible_values = list({repr(x) for x in signal_samples})

            # Append to text signal info dict
            text_signals_info[signal_name] = {"possible_values": possible_values, "unit":unit}
     
    
    signals_info = {"numeric_signals_info": numeric_signals_info, 
                    "text_signals_info": text_signals_info}
    
    # Save
    print(f"Saving: {yaml_filepath} ...")
    with open(yaml_filepath, 'w') as yaml_file:
        yaml.dump(signals_info, yaml_file, default_flow_style=False)