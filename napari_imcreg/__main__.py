import napari
import sys

from PIL import Image
from napari_imc import IMCController
from napari_imcreg import IMCRegController, IMCRegControllerException
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QMessageBox

# fix DecompressionBombWarning for large images
Image.MAX_IMAGE_PIXELS = None


def main() -> int:
    with napari.gui_qt() as app:
        source_viewer = napari.Viewer(title='Source')
        source_imc_controller = IMCController(source_viewer)
        source_imc_controller.initialize(show_open_imc_file_button=False)

        target_viewer = napari.Viewer(title='Target')
        target_imc_controller = IMCController(target_viewer)
        target_imc_controller.initialize(show_open_imc_file_button=False)

        def close_and_quit():
            source_viewer.close()
            target_viewer.close()
            QTimer().singleShot(1000, app.quit)

        try:
            controller = IMCRegController(source_imc_controller, target_imc_controller)
            controller.initialize()
            if controller.show_dialog():
                controller.show()
            else:
                close_and_quit()
                return 1
        except IMCRegControllerException as e:
            # noinspection PyArgumentList
            QMessageBox.critical(source_viewer.window.qt_viewer, 'IMCReg error', str(e))
            close_and_quit()
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
