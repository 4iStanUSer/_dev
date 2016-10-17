

def weeks_to_445(values_weekly, aggregator):
    # Init variables.
    values_445 = []
    start = 0
    end = 0
    months_counter = 0
    # Loop through list until it ends
    while True:
        # Determine months length
        if months_counter % 3 == 2:
            month_len = 5
        else:
            month_len = 4
        # Calculate end index of month
        end = start + month_len
        # Check if still in range of list
        if end > len(values_weekly):
            break
        # Apply aggregation function. Add month value to collection.
        values_445.append(aggregator(values_weekly[start:end]))
        # Calculate start index of next month
        start = end
        # Increase loop counter
        months_counter += 1
    # Return resulting list
    return values_445
