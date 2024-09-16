from asammdf import MDF, Signal
    

def resample_and_save_vsignalyzer(vsignalyzer_filepath: str, 
                                  mf4_filepath: str):
    # Load the mf4 file
    mdf = MDF(vsignalyzer_filepath)
    

    print(f"Resampling {vsignalyzer_filepath} ...")
    
    # Resample on a common timebase [0.1 seconds in this case]
    mdf = mdf.resample(0.1)

    # Try this - it will fail since there is a duplication of channel within different
    # signal groups
    try:
        mdf.get('VehicleMode').samples
    except Exception as e:
        print(f"The channel could not be read due to the following exception {e}")

    # Configure to not raise exception when accessing channels with multiple occurrences
    # This needs to be baked in the system prompt
    print("Set mdf raise_on_multiple_occurrences to false ...")
    mdf.configure(raise_on_multiple_occurrences=False)

    channels_list = list(set([channel['name'] for group in mdf.groups for channel in group['channels']]))

    # Append time signal as time
    if "t" in channels_list: 
        mdf.append(Signal(samples=mdf.get('t').samples, timestamps=mdf.get('t').timestamps, name='time'))

    # Try this - it will not fail, since the exception handling takes care of this
    mdf.get('VehicleMode').samples

    # Close the connection to the mf4 file

    print(f"Saving resampled mf4: {mf4_filepath}")
    mdf.save(mf4_filepath, overwrite=True)