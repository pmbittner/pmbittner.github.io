---
layout: page
title: BroT
description: encoding at-most-k constraints in boolean logic to configure branches of study
img: 
img-background: "white"
importance: 4
category: Software Variability
related_publications: true
language: Java
publications:
  - key: BTS:SEFM19
---


This project was an idea of my PhD supervisor [Thomas](https://www.tu-braunschweig.de/isf/team/thuem).
Back when I was in my master's at the Technical University Braunschweig, he was looking for a student to help in encoding the university's constraints for branches of study in computer science.
The premise is the following:

- In the computer science masters back then, you could choose a specialization such as _algorithm engineering_, _database engineering_, _visual computing_, and so on, called _branches of study_. To specialize, you had to select courses and lectures according to specific constraints, such as _"at least 20 credit points must be achieved from this subset of computer vision lectures"_. The constraints of each branch of study were defined in natural language on the universities website. Of course we found inconsistencies, ambiguities, and false-optional courses (i.e., a course may be flagged as optional, yet you _must_ take it to satisfy the constraints).
- Thomas was one of the lead developers of [FeatureIDE](https://featureide.github.io/), basically a reasoning-framework for boolean constraints, including an editor for [feature models](https://featureide.github.io/slides/featureide-0-background.pdf) to model constraints graphically (and more things but these are not important for our story here). So Thomas' idea was to reuse the reasoning engine to (1) formalize the branches of study, and (2) develop a configurator for students so they could see what courses to take (even if they already had taken some but not all relevant courses) and so on.

So I started working on this in terms of a project thesis, which later turned out into a paper {% cite BTS:SEFM19 %}. What I did was to...

1. ... develop a text-based domain-specific language (DSL) with editor support in Eclipse to specify branches of study. The DSL featured german keywords so that the administrative staff could write their own branches (which of course _never_ happened). Below is a small excerpt for the branch of `Big Data Management`, one of the simplest branches of study. Other branches were much more involved and the DSL also featured ways to specify the set of courses and their credit points and so on.
  ```java
  Studiengang "Computer Science"
    Studienrichtung "Branch Big Data Management"
      Pflicht
        "Relational Data Bases II"
        "Data Warehousing & Data Mining Techniques"
        "Master Thesis Information Systems"

      Wahlpflicht 30 CP
        "Project Thesis Information Systems"
        "Seminar Informationssysteme"
        "Digital Libraries"
        "Spatial Databases and Geo-Information Systems"
        "Distributed Data Management"
        "Wissensbasierte Systeme und deduktive Datenbanksysteme"
        "Multimedia-Datenbanken"
        "Information Retrieval & Web Search"
        "Ausgewählte Themen der Informationssysteme"
  ```

2. ... develop a compiler that converts expressions of my DSL to graphical feature models. The idea was that in the DSL, it would be easy to specify constraints where you have to select a subset of courses to reach a certain amount of credit points (`Wahlpflicht`), where it is hard to to the same in boolean logic - causing an exponential blowup in the worst case. Indeed, in the following feature model, the second constraint is cut off (`...`) because it is way too long.
  ![BigDataManagementFeatureModel](../../assets/img/brot_bigdata_fm.png "Big Data Management Feature Model")

3. ... develop a graphical application for students to determine which courses they would like to attend and for which branches they would be eligible. The tool could also tell students which courses to select to make a certain branch and so on. In the background, this was reusing the configuration engine of FeatureIDE, which uses decision propagation for these purposes:

Maybe I over-engineered this a bit but for sure it was fun.

In the end, the compilation and configuration did not scale well because of the aforementioned combinatorial explosion. While I could compile all branches, configuring some of them was just not feasible because the formulas were just too massive for the SAT solver. Using a better language such as higher-order logic and SMT solvers would have been more appropriate I guess but we wanted to see if we could reuse the FeatureIDE tooling for this particular problem without having to develop all the infrastructure from ground up.

So what's in here for you?
- The **compilation process** is outlined in detail in our **paper** {% cite BTS:SEFM19 %}. Here, we also explain how to encode at-most-k constraints based on a range of encodings from the literature, and we also present our own **meta at-most-k encoding**.
- If you are interested in **reusing the encoding implementation**, please check out our example repository on how to use the Java library:

<div class="row justify-content-sm-center">
{% include repository/repo.liquid repository="SoftVarE-Group/BroTLibraryExample" %}
</div>

- If you are interested in the **DSL**, the **compiler implementation**, or the **configuration tool**, please head to our official BroT repository:

<div class="row justify-content-sm-center">
{% include repository/repo.liquid repository="SoftVarE-Group/BroT" %}
</div>

_Oh, and BroT means Branch Of study Tool. (I wanted a cool name for the FOSD Cool Wall. Scroll down on [Christian Kästner's website](https://www.cs.cmu.edu/~ckaestne/) to learn more about it.)_
