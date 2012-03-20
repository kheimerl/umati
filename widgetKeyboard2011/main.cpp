#include <QtGui/QApplication>
#include "mainwindow.h"
#include "tester.h"

int main(int argc, char *argv[])
{
        QApplication    app(argc, argv);
        QTranslator     qtTranslator, myTranslator;
	QApplication::setApplicationName("widgetKeyboard");

	if (qtTranslator.load("qt_" + QLocale::system().name(), QLibraryInfo::location(QLibraryInfo::TranslationsPath)))
            app.installTranslator(&qtTranslator);
	else
            qDebug("Failed to load a translation for QT in your local language");
        if (myTranslator.load("virtualBoard_" + QLocale::system().name(), QCoreApplication::applicationDirPath()))
            app.installTranslator(&myTranslator);
	else
            qDebug("Failed to load a translation for the application");

	// the translator must be created before the application's widgets.

        Tester w;
#if defined(Q_WS_S60)
	w.showMaximized();
#else
	w.show();
#endif
	return app.exec();
}
