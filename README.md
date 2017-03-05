# infoglue-connector
> Keep your components local

## Installing
> To install simply run:

        python setup.py install

> If you are a developer, run:

        python setup.py develop

> instead.


## Using
> Using this little software is easy.

* Create a directory for your project
* Create another directory called `components` inside that directory.
* Create a `config.json` file where you are standing, it should look like
the one included in this repository called `config.example.json`.
* Download a component by running:

        infoglueget --id <component_id> --dir ./components

* Start the infoglue-dog / watchdog:

        infogluewatch --dir ./

> The watchdog will now look for changed made to components inside the
> `components/` directory, if a change has been made, it will push it to the
> server.
