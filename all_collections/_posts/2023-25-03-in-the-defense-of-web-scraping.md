---
layout: post
title: In defence of web scraping
date: 2023-25-03 10:18:00
tags: philosophy
---

SOURCE:

- [Open internet](https://hackernoon.com/web-scraping-and-the-fight-for-the-open-internet-ly1o2t8i)
- [Big data and web scraping](https://hackernoon.com/the-evolution-of-big-data-and-web-scraping-mk1y3ucv)
- [Season 3 of westworld]()
- [Robots_exclusion_standard](https://en.wikipedia.org/wiki/Robots_exclusion_standard)
- [Search_engine_scraping](https://en.wikipedia.org/wiki/Search_engine_scraping)
- [TheProject](http://info.cern.ch/hypertext/WWW/TheProject.html)
- [Internet was not predicted](https://www.youtube.com/watch?v=F4o3StI_NXo)
- [The Internet](https://www.youtube.com/watch?v=82m2du-zgmY)

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/service.png)</span>

When I mention to others that I'm working on "web scraping" for my personal project, they either don't understand what I'm referring to or react with apprehension. The term "web scraping" carries a negative connotation these days, often being perceived as unethical or even illegal.

# Why illegal?

Some companies might even take legal action against you (there have been numerous lawsuits related to web scraping over the years) or engage in lobbying efforts to outlaw it. While these efforts may not be successful, they can create a deterrent effect: individuals might feel guilty for engaging in potentially illegal activities.

# Why unethical?

Naturally, if you follow the news, you might think of incidents involving Cambridge Analytica or similar organizations that scrape social media user data and manipulate public opinion through targeted advertisements and the dissemination of fake news.

Today, it is evident that web scraping can be used to sell data to governments, industries, advertising companies, or even to influence election outcomes. Such practices are undoubtedly harmful, as the ultimate goal is control and manipulation, pushing people to buy or vote for someone who has paid for their support. If the sole objective is money, power, and control, the internet will become saturated with advertisements and surveillance. In this scenario, the web loses its meaning, and data is merely a tool for controlling people. Season 3 of Westworld and Episode 1 of Season 3 of Black Mirror provide fitting examples of the consequences we should strive to avoid.

<p style="text-align:center"><iframe width="100%" height="315" src="https://www.youtube.com/embed/YrpK90bHO2U" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></p>

If the goal is to have a centralized system that monitors everything and data with a single owner, it requires an approach similar to Facebook's, where users provide their data through an authentication system. When the technological architecture is designed in this manner, the data belongs exclusively to the company. By choosing to place all user-collected data behind an authentication system, the decision is made to retain the data rather than share it with others.

While these concerns are valid, it doesn't mean that web scraping should be entirely condemned. It might be worthwhile to reevaluate this practice and explore whether its direction can be changed for the better.

To achieve this, we must first revisit the fundamentals and appreciate the incredible nature of the web itself.

# What is the web?

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/document.png)</span>

<p style="text-align:center"><iframe width="100%" height="315" src="https://www.youtube.com/embed/_mNOXDbXr9c" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></p>

Essentially, the web consists of interconnected documents (where clicking on a link directs you to another document from a specific computer). These linked documents can be displayed by requesting a specific computer to download them to your browser using an HTTP/HTTPS protocol.

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/http.png)</span>

These computers are referred to as 'servers' because they are set up to listen for and respond to our requests. 'Servers' run a program in the background, awaiting incoming messages, so they can provide the requested document or data.

This may be a fundamental definition of what we know as the web. Its tremendous value today lies in the fact that all these documents, originating from various computers, are interconnected (with hyperlinks). Similar to university papers or academic books, they often include source references.

It is crucial to emphasize that there is no central super-computer overseeing all these documents. Likewise, there are no super-computers managing all the individual computers. Instead, information is distributed horizontally in a decentralized manner across various computers.

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/decentralized.png)</span>

Despite the level of control exerted by institutions, companies, and states in the physical world, no single entity holds absolute authority over the online world. In fact, some argue that the web has intentionally been designed to be uncontrollable, not necessarily by the US army, but rather by each person who contributes document files to the web.

In essence, the web can be likened to an extensive library of interconnected documents with no single owner. If data had owners and strict copyright laws, it would be impossible to construct a search engine. The web would then become a disorderly library with no reliable way of locating the documents that users require.

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/library.jpeg)</span>

# What is web scraping now?

<em>"The largest public known incident of a search engine being scraped happened in 2011 when Microsoft was caught scraping unknown keywords from Google for their own, rather new Bing service. But even this incident did not result in a court case."</em>

<em>"One possible reason might be that search engines like Google are getting almost all their data by scraping millions of public reachable websites, also without reading and accepting those terms. A legal case won by Google against Microsoft would possibly put their whole business as risk."</em>

[Wikipedia: Search engine scraping](https://en.wikipedia.org/wiki/Search_engine_scraping)

Web scraping is an automated method of gathering data from the internet. When an API is unavailable, the process typically involves extracting data from a website's HTML file, identifying the relevant information, and saving it to a database. Once the data is publicly available on the web, it can be stored, monitored, and utilized by anyone.

<p style="text-align:center"><video width="100%" height="500" controls> <source src="{{site.baseurl}}/assets/google2.mp4" type="video/mp4"> </video></p>

One of the co-founders of Google had a vision of downloading all the HTML documents on the web and creating a massive network of nodes based on the links found within each document. To accomplish this, he would need to develop a rule that identifies links within web pages, converts them into nodes, and determines their position within the network.

We can easily see here that Google is today’s most advanced web scraping company in existence. And, if we really want to access it, Google’s web scraping gives us the most amazing access to culture (with a big C) that there is.

It's evident that Google is currently the most advanced web scraping company (using web crawling), and their web scraping technology provides unparalleled access to culture (with a capital C) on the internet.

# No Web Scraping, no search engine

<p style="text-align:center"><video width="100%" controls> <source src="{{site.baseurl}}/assets/google4.mp4" type="video/mp4"> </video></p>

To navigate the vastness of the internet, search engines like Google are crucial. Without them, finding information and resources would be incredibly difficult, and we would be limited to only accessing content from highly influential individuals or powerful companies who have the means to promote their content.

<p style="text-align:center"><video width="100%" height="500" controls> <source src="{{site.baseurl}}/assets/google.mp4" type="video/mp4"> </video></p>

# So now where can we go?

Today, many of us still underestimate the full potential of web scraping, perhaps because it is not an easy technique to master. Typically, we tend to associate web scraping with finding cheap deals on flights, restaurants, and products, which is certainly useful. However, there may be other, even more valuable applications for web scraping.

In particular, the web is uniquely suited to handle big data, which is essential for machine learning. Without the web, there would be no big data, and without big data, machine learning would be impossible. With the increasing power of computers, we now have access to machine learning techniques that can scrape the web, classify and process vast amounts of data, and extract meaningful insights. This opens up many exciting possibilities, including:

- [AI can help doctors diagnose diseases more accurately and quickly by analyzing medical images, symptoms, and patient history]()
- [AI can help predict and mitigate the effects of climate change by analyzing data from weather sensors, satellite imagery, and other sources]()
- [AI can help emergency responders better respond to natural disasters by analyzing data from sensors, social media, and other sources]()
- [AI can detect fraudulent activity in financial transactions and prevent it from happening in the first place]()
- [AI can help monitor and protect the environment by analyzing data on pollution, deforestation, and other factors]()
- [AI can be used to optimize energy usage and reduce carbon emissions in industries like transportation, manufacturing, and agriculture]()
- [automatized customer services that use advanced chatbots to problem-solve help you mend stuff (by sending photos to them) and find what you need to buy for you]()
- [AI can help people with disabilities by improving accessibility, creating custom devices and technologies]()
- [machine learning can give us very precise statistics in economy, urbanism, criminality]() …
- [AI can help farmers optimize their crops and reduce waste by providing insights into soil quality, weather patterns, and crop health]()
- [AI can assist scientists in analyzing vast amounts of data, modeling complex systems and predicting outcomes, and facilitating collaborations across research communities]()
- [AI can automate repetitive tasks, streamline workflows, and provide data-driven insights to help employees work more efficiently]()
- [AI could be used to manage and optimize decentralized renewable energy grids. This could involve predicting energy supply and demand, managing energy storage systems, and balancing energy usage across a network of decentralized generators and consumers]()
- [AI could be used to optimize building energy efficiency by analyzing data on building usage patterns and adjusting heating, ventilation, and lighting systems accordingly]()

  ...

Other suggestions?

Web scraping is useful here because we need classified data to detect something. For example, we can scrap images of skin cancer everywhere on the web and classify to automatically detect it on a random photo. We can scrap images of forest fires so that cameras can recognize a danger automatically.

In summary, Web scraping can give us better access to culture, science, and with better access to culture, science... humans can maybe act in the world with greater attention to important things and/or awareness.
