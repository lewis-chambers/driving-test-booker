# Driving Test Cancellation Search
This command line app was developed to automatically navigate the GOV driving test booking website in the UK. When a driving test is cancelled, the slot becomes available for anyone to swap to or book.
## Operation
The app operates in a constant loop, recognising the current page and the current task to do.

For example. When the current directive is to log in, it will navigate to the login page and sign in. If a recaptcha pops up, it will wait for user input.

It is designed to appear very human, interacting with the website at a modest speed with random delays.

## Notes
The booking website can only be accessed if you have a test booked already.

This app was developed and used to get my test moved up by months in August 2021. I can no longer access the website to test further, so some debugging may need to be done, depending on when this is accessed.

## Roadmap

This bit of software could reasonably be monetised if a solution for solving the recaptchas is found - like a solving service. However, I'm not interested to do so right now. Furthermore, I expect that in time, the booking website will have changed to some extent, depreciating elements of the program. I cannot access the site anymore, so I will not be maintaining it.
