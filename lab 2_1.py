import folium

m = folium.Map(location=[48.8350125, 24.0197128],
               zoom_start=12)

tooltip = 'Класни на мене!'

folium.Marker([49.822994, 24.035093], popup='УКУ Свєнціцького', tooltip=tooltip).add_to(m)
folium.Marker([49.817443, 24.0197128], popup='УКУ Свєнціцького', tooltip=tooltip).add_to(m)

m.save('Map_1.html')


