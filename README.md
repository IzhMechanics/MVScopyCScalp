# MVScopyCScalp
### Перенос настроек тикеров из Привод Бондаря версия 2.9.7.0 в CScalp версия 2.11.2.0
___<img width="592" height="325" alt="mvscopy" src="https://github.com/user-attachments/assets/a6dd769a-19da-4069-91c7-3a348d634c6e" />

   1. **Вариант 1** Сначало установите новый привод, настройте рабочие пространства,  
     поставьте тикеры в стаканы (но не настраивайте тикеры) и закройте привод  
     **Вариант 2** Или не запускайте после установки новый привод, а скопируйте содержимое папки mvs архива **MVS.7z**  
     в \FSR Launcher\SubApps\CS\Data\MVS

   3. Запустите MVScopy.exe и укажите ваши настройки из старого привода (Исходная папка)  
   C:\Program Files (x86)\FSR Launcher\SubApps\PrivodBondar\Data\MVS

   4. Укажите настройки из нового привода (Целевая папка)  
   C:\Program Files (x86)\FSR Launcher\SubApps\CS\Data\MVS

   5. *не тестировалось на других версиях
   6. **кластера устанавливаются как дельта "Color_AmountDelta"  
   **можете использовать вручную **MVScopy-manually.py** прописав папки в конце скрипта  
    if __name__ == "__main__":  
     source_dir = os.path.abspath('исходная папка')  
     target_dir = os.path.abspath('целевая папка')  

   ## Donate
   Попросили добавить донат, посмотрим сколько стоит ваше время 
   
   BSC (BEP20)
   ```
   0xddcbe9f84e455fb920a5ba63b4ff023ffe7f9f72
   ```
   TON
   ```
   UQB9ox7Lx85ewqlMkD52qOjsfM-s03frtPBXzrzkgbX_nyn5
   ```
   APTOS
   ```
   0xfa91c8dd813a43be92117565fe49d0cde224882304d85d53469a31665b284436
   ```
   TRON (TRC20)
   ```
   TBJz8hVW9s4oMdiPqadY7GoB4uDFH4QGSV
   ```
