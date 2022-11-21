# Driving Test Cancellation Search
This command line app was developed to automatically navigate the GOV driving test booking website in the UK. When a driving test is cancelled, the slot becomes available for anyone to swap to or book.

## How to Use

To use the code do the following:


1. Create a new venv.
```
python -m venv <environment>
```

2. Clone the repo into the venv

```
cd <environment>
git clone https://github.com/lewis-chambers/driving-test-booker.git driving-test-booker

```

3. Activate venv and install `requirements.txt`

```
cd <environment>
Source bin/activate
python -m pip install -r driving-test-booker/requirements.txt
```

4. Make a credentials file

Make a file called `credentials.env` in the following
format:

```
LICENCE=<your driving licence>
REFERENCE=<your test reference>
```
Make sure it's loaded by the `load_dotenv_file` method.

4. Run the script.

```
cd <environment>
python -m main_script.py
```

5. Customise the crawler randomness.

At points in the script youll see `RandomWait(x, y)`. This adds a random wait time in the range supplied, change these as you like.  The wider the range, the less likely you are to get detected.

## Operation
The app operates in a constant loop, recognising the current page and the current task to do.

For example. When the current directive is to log in, it will navigate to the login page and sign in. If a recaptcha pops up, it will wait for user input.

It is designed to appear very human, interacting with the website at a modest speed with random delays.

## Notes
The booking website can only be accessed if you have a test booked already.

This app was developed and used to get my test moved up by months in August 2021. I can no longer access the website to test further, so some debugging may need to be done, depending on when this is accessed.

## Roadmap

This bit of software could reasonably be monetised if a solution for solving the recaptchas is found - like a solving service. However, I'm not interested to do so right now. Furthermore, I expect that in time, the booking website will have changed to some extent, depreciating elements of the program. I cannot access the site anymore, so I will not be maintaining it.
