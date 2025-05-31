ws['F42'] = cooling1_glycol if (cooling1_type == 'Водяний'
                                    and type_ahu in ['Припливна', 'Припливно-витяжна']) else None
ws['F47'] = cooling2_glycol if (cooling2_type == 'Водяний'
                                    and type_ahu in ['Припливна', 'Припливно-витяжна']
                                    and confirm_cooling2 == 'Так') else None

ws['F42'] = freon1 if (cooling1_type == 'Фреоновий'
                                            and type_ahu in ['Припливна', 'Припливно-витяжна']) else None
ws['F47'] = freon2 if (cooling2_type == 'Фреоновий'
                           and type_ahu in ['Припливна', 'Припливно-витяжна']
                           and confirm_cooling2 == 'Так') else None