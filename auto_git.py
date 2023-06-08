import os
import sys
import time


def extract_requirements():
    os.system('pip freeze > requirements.txt')


def github_commit():
    commit_message = input('commit message : ')
    os.system('git add -A')
    os.system('git commit -m "{}"'.format(commit_message))


def migrate_for_server():
    print('Makemigrations Start')
    os.system('python manage.py makemigrations --settings config.settings.product')
    print('Makemigrations Finished')
    time.sleep(2)
    print('Migrate Start')
    os.system('python manage.py migrate --settings config.settings.product')
    print('migrate Finished')


def wait_railway():
    minute = 2
    seconds = 60 * minute
    for second in range(seconds+1,0,-1):
        sys.stdout.flush()
        print(f"\rWait for Railway Deploy | Estimated > {second}.Second left", end=" ")
        time.sleep(1)


def github_push():
    section = input('do you want push Y/n')
    if not section.lower() == 'n':
        os.system('git push')

    print('Update Finished')


def main():
    sections = '>AutoGithub♥\n1.Multi(commit+req.txt/push)\n2.Commit\n3.Push\n4.Req.txt extract\n5.1+sync\n6.sync\nyou@AutoGithub : '
    section = input(sections)

    if section == '1':
        extract_requirements()
        github_commit()
        github_push()
    if section == '2':
        github_commit()
    if section == '3':
        github_push()
    if section == '4':
        extract_requirements()
    if section == '5':
        extract_requirements()
        github_commit()
        github_push()
        wait_railway()
        migrate_for_server()
    if section == '6':
        migrate_for_server()


if __name__ == '__main__':
    main()

