import flet as ft

def main(page: ft.Page):
    page.title = "Calculadora de Costos VPS"
    page.window.width = 500
    page.window.height = 800
    
    # Cargar el tema guardado o usar oscuro por defecto
    def load_theme_preference():
        try:
            # Intentar cargar desde el cliente
            theme_data = page.client_storage.get("theme_mode")
            if theme_data is not None:
                return ft.ThemeMode.DARK if theme_data == "dark" else ft.ThemeMode.LIGHT
        except Exception:
            pass
        # Si no hay preferencia guardada, usar modo oscuro
        return ft.ThemeMode.DARK
    
    # Establecer el tema inicial
    page.theme_mode = load_theme_preference()
    
    # Variables globales
    ram_value = 1
    cpu_value = 1
    ssd_value = 20
    dias_value = 30
    current_index = 0
    
    # Constantes de precios
    PRECIO_CPU = 0.04
    PRECIO_RAM = 0.05
    PRECIO_DISCO = 0.01
    PRECIO_TRANSFERENCIA = 250

    # Función para cambiar y guardar el tema
    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT 
            if page.theme_mode == ft.ThemeMode.DARK 
            else ft.ThemeMode.DARK
        )
        # Guardar la preferencia
        theme_value = "dark" if page.theme_mode == ft.ThemeMode.DARK else "light"
        page.client_storage.set("theme_mode", theme_value)
        # Actualizar el ícono del botón
        theme_button.icon = (
            ft.Icons.LIGHT_MODE 
            if page.theme_mode == ft.ThemeMode.DARK 
            else ft.Icons.DARK_MODE
        )
        page.update()
    
    # Actualizado para que los numeros de arriba  tambien actualicen
    def create_counter(label, unit, initial_value, min_value=1):
        # Text para el valor superior
        header_value = ft.Text(
            str(initial_value),
            size=20,
            weight=ft.FontWeight.BOLD,
        )
        
        def decrease(e):
            nonlocal initial_value
            if initial_value > min_value:
                initial_value -= 1
                # Actualizamos el texto del header
                header_value.value = str(initial_value)
                if label == "RAM":
                    nonlocal ram_value
                    ram_value = initial_value
                elif label == "CPU":
                    nonlocal cpu_value
                    cpu_value = initial_value
                elif label == "SSD":
                    nonlocal ssd_value
                    ssd_value = initial_value
                elif label == "DÍAS":
                    nonlocal dias_value
                    dias_value = initial_value
                calcular_costo()
                page.update()

        def increase(e):
            nonlocal initial_value
            initial_value += 1
            # Actualizamos el texto del header
            header_value.value = str(initial_value)
            if label == "RAM":
                nonlocal ram_value
                ram_value = initial_value
            elif label == "CPU":
                nonlocal cpu_value
                cpu_value = initial_value
            elif label == "SSD":
                nonlocal ssd_value
                ssd_value = initial_value
            elif label == "DÍAS":
                nonlocal dias_value
                dias_value = initial_value
            calcular_costo()
            page.update()

        return ft.Column(
            controls=[
                ft.Text(unit, size=12),
                ft.Row(
                    controls=[
                        header_value,
                        ft.Text(label, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(
                                ft.Icons.REMOVE,
                                on_click=decrease,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.BLUE,
                                ),
                            ),
                            ft.IconButton(
                                ft.Icons.ADD,
                                on_click=increase,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.BLUE,
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border_radius=10,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        )

    def calcular_costo(e=None):
        costo_cpu = cpu_value * PRECIO_CPU * 24
        costo_ram = ram_value * PRECIO_RAM * 24
        costo_disco = ssd_value * PRECIO_DISCO * 24
        
        costo_total = (costo_cpu + costo_ram + costo_disco) * dias_value
        
        if transferencia_check.value:
            costo_total += PRECIO_TRANSFERENCIA
            
        precio_total.value = f"{costo_total:.2f}$"
        page.update()

    precio_total = ft.Text(
        "0.00$",
        size=50,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE,
    )

    transferencia_check = ft.Checkbox(
        label="Transferencia adicional (+250 CUP)",
        on_change=calcular_costo
    )

    def build_home_view():
        return ft.Container(
            content=ft.Column(
                controls=[
                    precio_total,
                    ft.Row(
                        controls=[
                            create_counter("RAM", "GB", ram_value),
                            create_counter("CPU", "Unidad", cpu_value),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ),
                    ft.Row(
                        controls=[
                            create_counter("SSD", "GB", ssd_value),
                            create_counter("DÍAS", "24/h", dias_value),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ),
                    transferencia_check,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
            padding=20
        )

    def build_about_view():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Acerca de VPS Calculator",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE,
                    ),
                    ft.Text(
                        "Versión 1.0.0",
                        size=16,
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Esta aplicación te ayuda a calcular el costo de tu servidor virtual (VPS) "
                            "basado en los recursos que necesitas:\n\n"
                            "• RAM: 0.05 CUP/hora\n"
                            "• CPU: 0.04 CUP/hora\n"
                            "• Almacenamiento: 0.01 CUP/hora\n"
                            "• Transferencia adicional: 250 CUP\n\n"
                            "Desarrollado con Flet y Python. Por KeimaSenpai",
                            size=16,
                            text_align=ft.TextAlign.JUSTIFY,
                        ),
                        padding=20,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=20
        )

    container = ft.Container()

    def change_tab(e):
        nonlocal current_index
        current_index = e.control.selected_index
        
        if current_index == 0:
            container.content = build_home_view()
        else:
            container.content = build_about_view()
        
        page.update()

    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME,
                label="Home",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.INFO,
                label="About",
            ),
        ],
        adaptive=True,
        on_change=change_tab,
        selected_index=0,
    )

    # Crear el botón de tema con el ícono correcto según el tema actual
    theme_button = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE,
        on_click=toggle_theme,
    )

    container.content = build_home_view()
    page.appbar = ft.AppBar(
        leading_width=45,
        title=ft.Text("VPS Calculator", weight=ft.FontWeight.BOLD, size=20),
        # center_title=True,
        bgcolor=ft.Colors.BLUE,
        adaptive=True,
        actions=[theme_button],
    )
    
    page.add(
        container,
        navigation_bar,
    )
    
    calcular_costo()

ft.app(target=main)