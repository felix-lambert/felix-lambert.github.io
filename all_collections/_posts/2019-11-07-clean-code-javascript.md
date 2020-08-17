---
layout: post
title: Clean code javascript
date: 2019-11-07 10:18:00
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

The end goal of code is to be understood by a machine and by an other human being. This is like communication: like code, if you speak and no one understand you, you're only speaking to yourself and others cannot make any use of it.

Envisioning code as a story can be a useful metaphor for helping to create clean code. If the audience has difficulty reading your story, it will not be a pleasant experience for them. They will not be able to work with it, explain the nuances to others, or adapt it in the future.

So clean code is just simple code. Nothing else.

# Naming

## Use meaningful and pronounceable variable names

Bad:

```javascript
let d;
let elapsed;
const ages = arr.map(i => i.age);
```

Good:

```javascript
let daysSinceModification;
const agesOfUsers = users.map(user => user.age);
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
locations.forEach(l => {
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
locations.forEach(location => {
  doStuff();
  doSomeOtherStuff();
  // ...
  // ...
  // ...
  dispatch(location);
});
```

## Functions

Use default arguments instead of short circuiting or conditionals

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
