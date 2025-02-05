admins = {
    1: {'fullname': 'Abror Nurmatov', 'username': 'Abror_ds', 'age': '19', 'telephone_number': '+998931196001',
        'is_confirmed': 0, 'is_admin': 1},

    2: {'fullname': 'Xonzoda Karimova', 'username': 'Abror_ds', 'age': '18', 'telephone_number': '+998943215674',
        'is_confirmed': 0, 'is_admin': 1}
}
admin_usernames = []
for individual_dict_key, individual_dict_value in admins.items():
    for column in individual_dict_value:
        if column == 'username':
            admin_usernames.append(individual_dict_value[column])

print(admin_usernames)
