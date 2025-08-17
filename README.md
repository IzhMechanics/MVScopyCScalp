# MVScopyCScalp
### Перенос настроек тикеров из Привод Бондаря версия 2.9.7.0 в CScalp версия 2.11.2.0

1. Сначало установите новый привод, настройте рабочие пространства, поставьте тикеры в стаканы (но не настраивайте тикеры)

2. Запустите MVScopy.exe и укажите ваши настройки из старого привода (Исходная папка)
   C:\Program Files (x86)\FSR Launcher\SubApps\PrivodBondar\Data\MVS

4. Укажите настройки из нового привода (Целевая папка)
   C:\Program Files (x86)\FSR LauncherNew\SubApps\CS\Data\MVS

*не тестировалось на других версиях
**кластера устанавливаются как дельта "Color_AmountDelta"
**можете использовать вручную MVScopy-manually.py прописав папки в конце скрипта
if __name__ == "__main__":
    source_dir = os.path.abspath('исходная папка')
    target_dir = os.path.abspath('целевая папка')
