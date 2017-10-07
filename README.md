# RoboMission
RoboMission is an intelligent web application for learning computer science,
aiming at creating a [flow experience][1].
RoboMission is developed by [Adaptive Learning group][2] at Faculty of informatics, Masaryk university.

  [1]: https://en.wikipedia.org/wiki/Flow_(psychology)
  [2]: http://www.fi.muni.cz/adaptivelearning/

## Start working on the project

1. Install Python 3.5, virtualenv, virtualenvwrapper and npm.

2. Configure virtualenv and virtualenvwrapper by adding the following two lines in your `~/.bashrc`:

        export WORKON_HOME=~/.virtualenvs
        source --python=/usr/bin/python3.5 /usr/bin/virtualenvwrapper.sh

  Load the changes:

        $ source ~/.bashrc

3. Clone the project repository:

        $ git clone https://github.com/adaptive-learning/robomission.git

4. Create virtual environment and bind it with the project directory:

        $ cd robomission
        $ mkvirtualenv robomission && setvirtualenvproject

  The name of the virtual environment (robomission) should now appear in front of the prompt.

5. Install dependencies and initialize DB:

        $ make install

  The `make install` command uses pip to install install backend dependencies,
  npm for frontend dependencies,
  and then it sets up the database for development. (See Makefile for details.)
  You can deactivate the virtual environment by calling `deactivate`.

## Workflow

1. Start the virtual environment and jump to the project directory:

        $ workon robomission

2. Pull the changes from the repository.

        $ git pull

3. Update dependencies and database:

        $ make update

4. Create and checkout a git branch for the implemented feature.

        $ git checkout -b name_of_the_feature

5. Write unit tests for the implemented feature (and possibly integration tests as well).
  Check that the tests don't pass.

        $ make test

6. Develop the feature. Enjoy it, experience the state of flow :-)

  * To start a server, run:

          $ make server

  *  To open python console (with all models automatically imported), run:

          $ make shell

  *  To open jupyter notebooek, run:

          $ make notebook

  * If you change data in fixtures and want to load them to the database:

          $ make db-load-data

  * If you change the data model, create and apply a migration:

          $ ./manage.py makemigrations
          $ ./manage.py migrate

  * Take a regular breaks (e.g. after 25 minutes), stretch yourself (including your eyes).

8. Test the implemented feature and check the code by a linter:

        $ make test
        $ make lint

9. Commit changes:

        $ git add changed_files
        $ git commit -m "Implement feature X"

10. Merge the feature branch to the master branch:

        $ git checkout master
        $ git merge name_of_the_feature

11. Push changes to the GitHub:

        $ git push

12. Deactivate the virtual environment:

        $ deactivate

13. Celebrate the developed feature with some physical exercise and healthy snack.
