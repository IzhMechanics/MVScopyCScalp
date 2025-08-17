# MVScopyCScalp
### Перенос настроек тикеров из Привод Бондаря версия 2.9.7.0 в CScalp версия 2.11.2.0
___<img width="592" height="325" alt="mvscopy" src="https://github.com/user-attachments/assets/a6dd769a-19da-4069-91c7-3a348d634c6e" />

1. Сначало установите новый привод, настройте рабочие пространства, поставьте тикеры в стаканы (но не настраивайте тикеры)  

2. Запустите MVScopy.exe и укажите ваши настройки из старого привода (Исходная папка)  
C:\Program Files (x86)\FSR Launcher\SubApps\PrivodBondar\Data\MVS

3. Укажите настройки из нового привода (Целевая папка)  
   C:\Program Files (x86)\FSR LauncherNew\SubApps\CS\Data\MVS

4. *не тестировалось на других версиях  
**кластера устанавливаются как дельта "Color_AmountDelta"  
**можете использовать вручную **MVScopy-manually.py** прописав папки в конце скрипта  
    if __name__ == "__main__":  
     source_dir = os.path.abspath('исходная папка')  
     target_dir = os.path.abspath('целевая папка')  

