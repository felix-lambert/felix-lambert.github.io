---
layout: post
title: Clean code javascript
date: 2022-28-03 10:18:00
tags: technology
---

SOURCE:

- [https://github.com/airbnb/javascript](https://github.com/airbnb/javascript)
- [https://google.github.io/styleguide/jsguide.html](https://google.github.io/styleguide/jsguide.html)
- [https://medium.com/@konstankino/2019-reactjs-best-practices-design-patterns-516e1c3ca06a](https://medium.com/@konstankino/2019-reactjs-best-practices-design-patterns-516e1c3ca06a)
- [https://americanexpress.io/clean-code-dirty-code/](https://americanexpress.io/clean-code-dirty-code/)
- [https://dmitripavlutin.com/react-usestate-hook-guide/](https://dmitripavlutin.com/react-usestate-hook-guide/)
- [https://lightsonsoftware.com/writing-code-that-reads-like-a-story/](https://lightsonsoftware.com/writing-code-that-reads-like-a-story/)
- [https://opensource.com/business/15/10/jane-austen-on-python](https://opensource.com/business/15/10/jane-austen-on-python)
- [https://eloquentjavascript.net/Eloquent_JavaScript.pdf](https://eloquentjavascript.net/Eloquent_JavaScript.pdf)

At its core, the ultimate objective of code is to be comprehensible by both machines and humans alike. If you communicate ideas in a way that only you can understand, it becomes impractical for others to utilize or build upon your work. Therefore, when creating a variable or any other code, it is crucial to consider whether it will enhance the readability and predictability of the code for the next developer. This helps to ensure that the code is easily understood and maintainable, facilitating collaboration and progress.

Metaphorically viewing code as a story can be an effective way to create clean and comprehensible code. Just as a poorly written story can be difficult for an audience to read and understand, code that is not easy to read can be a frustrating experience for developers. If the code is unclear or convoluted, it becomes challenging to work with, explain to others, and adapt in the future. Therefore, striving to write code that tells a clear and concise story can improve its readability and facilitate collaboration and progress.

Clean code can be summed up as simple code, nothing more. Even if you find yourself repeating certain code segments without abstraction, as long as the code remains straightforward and uncomplicated, it doesn't matter.

# Naming

## Use meaningful and pronounceable variable names

Bad:

```javascript
let d;
let elapsed;
const ages = arr.map((i) => i.age);
```

Good:

```javascript
let daysSinceModification;
const agesOfUsers = users.map((user) => user.age);
```

## Make meaningful distinctions and don't add extra, unnecessary nouns to the variable name

Bad:

```javascript
let nameString;
let theUsers;
```

Good:

```javascript
let name;
let users;
```

## Make your variable names easy to pronounce, because for the human mind it takes less effort to process

In short, don't cause extra mental mapping with your names.

Bad:

```javascript
let fName, lName;
let cntr;

let full = false;
if (cart.size > 100) {
  full = true;
}
```

Good:

```javascript
let firstName, lastName;
let counter;

const MAX_CART_SIZE = 100;
// ...
const isFull = cart.size > MAX_CART_SIZE;
```

## Use searchable names

We will read more code than we will ever write. It's important that the code we do write is readable and searchable. By not naming variables that end up being meaningful for understanding our program, we hurt our readers. Make your names searchable.

Bad:

```javascript
// What the heck is 86400000 for?
setTimeout(blastOff, 86400000);
```

Good:

```javascript
// Declare them as capitalized named constants.
const MILLISECONDS_IN_A_DAY = 86400000;

setTimeout(blastOff, MILLISECONDS_IN_A_DAY);
```

## Use explanatory variables

Bad:

```javascript
const address = "One Infinite Loop, Cupertino 95014";
const cityZipCodeRegex = /^[^,\\]+[,\\\s]+(.+?)\s*(\d{5})?$/;
saveCityZipCode(
  address.match(cityZipCodeRegex)[1],
  address.match(cityZipCodeRegex)[2]
);
```

Good:

```javascript
const address = "One Infinite Loop, Cupertino 95014";
const cityZipCodeRegex = /^[^,\\]+[,\\\s]+(.+?)\s*(\d{5})?$/;
const [, city, zipCode] = address.match(cityZipCodeRegex) || [];
saveCityZipCode(city, zipCode);
```

## Avoid Mental Mapping

Explicit is better than implicit.

Bad:

```javascript
const locations = ["Austin", "New York", "San Francisco"];
locations.forEach((l) => {
  doStuff();
  doSomeOtherStuff();
  // ...
  // ...
  // ...
  // Wait, what is `l` for again?
  dispatch(l);
});
```

Good:

```javascript
const locations = ["Austin", "New York", "San Francisco"];
locations.forEach((location) => {
  doStuff();
  doSomeOtherStuff();
  // ...
  // ...
  // ...
  dispatch(location);
});
```

## Use the same vocabulary for the same type of variable

Bad:

```javascript
getUserInfo();
getClientData();
getCustomerRecord();
```

Good:

```javascript
getUser();
```

## Function names should say what they do

Use long, descriptive names. A long descriptive name is way better than a short, enigmatic name or a long descriptive comment.

Bad:

```javascript
function addToDate(date, month) {
  // ...
}

const date = new Date();

// It's hard to tell from the function name what is added
addToDate(date, 1);
```

```javascript
function inv(user) {
  /* implementation */
}
```

Good:

```javascript
function addMonthToDate(month, date) {
  // ...
}

const date = new Date();
addMonthToDate(1, date);
```

```javascript
function inviteUser(emailAddress) {
  /* implementation */
}
```

## Functions should be named for what they do, not how they do it

Bad:

```javascript

const loadConfigFromServer = () => {
  ...
};
```

Good:

```javascript
// good
const loadConfig = () => {
  ...
};
```

# Don't indent unnecessarily

Too many nested indentations often create a distorted view of its complexity.

Bad:

```javascript
function processItems(list) {
  var result = [];

  if (items.length > 0) {
    normalize(items);
    for (var index = 0, len = items.length; index < len; ++index) {
      // long code…
    }
  }

  return result;
}
```

Good:

```javascript
function processItems(list) {
  var result = [];

  if (items.length <= 0) return result;

  normalize(items);
  for (var index = 0, len = items.length; index < len; ++index) {
    // long code…
  }

  return result;
}
```

# Functions

## Use default arguments instead of short circuiting or conditionals

Default arguments are often cleaner than short circuiting. Be aware that if you use them, your function will only provide default values for undefined arguments. Other "falsy" values such as '', "", false, null, 0, and NaN, will not be replaced by a default value.

Bad:

```javascript
function createMicrobrewery(name) {
  const breweryName = name || "Hipster Brew Co.";
  // ...
}
```

Good:

```javascript
function createMicrobrewery(name = "Hipster Brew Co.") {
  // ...
}
```

## Function arguments (2 or fewer ideally)

Usually, if you have more than two arguments then your function is trying to do too much. In cases where it's not, most of the time a higher-level object will suffice as an argument.
Since JavaScript allows you to make objects on the fly, without a lot of class boilerplate, you can use an object if you are finding yourself needing a lot of arguments.

Bad:

```javascript
function createMenu(title, body, buttonText, cancellable) {
  // ...
}
```

Good:

```javascript
function createMenu({ title, body, buttonText, cancellable }) {
  // ...
}

createMenu({
  title: "Foo",
  body: "Bar",
  buttonText: "Baz",
  cancellable: true,
});
```

## Functions should do one thing

This is by far the most important rule in software engineering. When functions do more than one thing, they are harder to reason about. When you can isolate a function to just one action, your code will read much cleaner.

Bad:

```javascript
function emailClients(clients) {
  clients.forEach((client) => {
    const clientRecord = database.lookup(client);
    if (clientRecord.isActive()) {
      email(client);
    }
  });
}
```

Good:

```javascript
function emailActiveClients(clients) {
  clients.filter(isActiveClient).forEach(email);
}

function isActiveClient(client) {
  const clientRecord = database.lookup(client);
  return clientRecord.isActive();
}
```

# Objects

## Don't add unneeded context

If your class/object name tells you something, don't repeat that in your variable name.
Bad:

```javascript
const Car = {
  carMake: "Honda",
  carModel: "Accord",
  carColor: "Blue",
};
```

```javascript
function paintCar(car) {
  car.carColor = "Red";
}
```

Good:

```javascript
const Car = {
  make: "Honda",
  model: "Accord",
  color: "Blue",
};

function paintCar(car) {
  car.color = "Red";
}
```

## Don't use flags as function parameters

Flags tell your user that this function does more than one thing. Functions should do one thing. Split out your functions if they are following different code paths based on a boolean.

Bad:

```javascript
function createFile(name, temp) {
  if (temp) {
    fs.create(`./temp/${name}`);
  } else {
    fs.create(name);
  }
}
```

Good:

```javascript
function createFile(name) {
  fs.create(name);
}

function createTempFile(name) {
  createFile(`./temp/${name}`);
}
```

## Encapsulate conditionals

Bad:

```javascript
if (fsm.state === "fetching" && isEmpty(listNode)) {
  // ...
}
```

Good:

```javascript
function shouldShowSpinner(fsm, listNode) {
  return fsm.state === "fetching" && isEmpty(listNode);
}

if (shouldShowSpinner(fsmInstance, listNodeInstance)) {
  // ...
}
```

## Avoid negative conditionals

Bad:

```javascript
function isDOMNodeNotPresent(node) {
  // ...
}

if (!isDOMNodeNotPresent(node)) {
  // ...
}
```

Good:

```javascript
function isDOMNodePresent(node) {
  // ...
}

if (isDOMNodePresent(node)) {
  // ...
}
```

# Error Handling

Thrown errors are a good thing! They mean the runtime has successfully identified when something in your program has gone wrong and it's letting you know by stopping function execution on the current stack, killing the process (in Node), and notifying you in the console with a stack trace.

# Build on the shoulders of giants

## React

### The DOM

We want to touch the DOM as little as possible. The DOM is a very complex API and rendering in browsers can take up a lot of time.

### Separate stateful aspects from rendering

Bad:

```javascript
class User extends Component {
  state = { loading: true };

  render() {
    const { loading, user } = this.state;
    return loading ? (
      <div>Loading...</div>
    ) : (
      <div>
        <div>First name: {user.firstName}</div>
        <div>First name: {user.lastName}</div>
        ...
      </div>
    );
  }

  componentDidMount() {
    fetchUser(this.props.id).then((user) => {
      this.setState({ loading: false, user });
    });
  }
}
```

Good:

```javascript
class User extends Component {
  state = { loading: true };

  render() {
    const { loading, user } = this.state;
    return loading ? <Loading /> : <RenderUser user={user} />;
  }

  componentDidMount() {
    fetchUser(this.props.id).then((user) => {
      this.setState({ loading: false, user });
    });
  }
}
```
