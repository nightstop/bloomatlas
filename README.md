# Bloom Atlas
**Bloom Atlas is built to improve the creative delivery of a design project, and it can also be a learning tool for anyone curious about plants and their flowering times. It is essentially a data visualisation project, with features that create a shared language for designers and clients to exchange ideas.**

**Source**:  AusTraits v7.0.0* is a CC-BY licensed open-access database. Data were modelled and filtered in Power BI to show flower colour, flowering time, Latin name, establishment, taxon distribution, genus and family. Flower colour and flowering time are the two core traits, each was structured into one row per species and the tables were later merged.

**Data analysis:** Grain: One row per species, using the binomial (Latin) name. A species-level name is what the shared-language and learning purpose needs for easy communication. Common names are not included in AusTraits v7.0.0.

Flowering months: One source dataset only (AusTraits v7.0.0: PlantNET, NSW), because flowering months can change based on location and the app doesn't include location selection.

Flower colour: Compiled from all sources into one row per plant in the model to show colour as a species trait.

**AI**: Claude code drafted the Python that converts the modelled table (exported as Parquet) into app's JSON. Also used for frontend creation and updating the final look. Reviewed, questioned and hand-corrected by human.

Deployed to Cloudflare Workers from the github repo.

**Result:**  3,614 plants (1,027 genera & 153 families) feeding a radial wheel that visualises flowering months and flower colours - up to 10 plants at once. Each wedge is a month, and each plant's flower colours stack within the months it flowers, showing which colours are present. 

**How to use:** Search by Latin name, or paint the wheel to explore. Click the centre of the wheel to randomise the plants shown. Click a plant name to open the plant card that shows the plant's genus, family, establishment(native/naturalised) and taxon distribution along with its flowering months and flower colours.

**Disclaimer:** Bloom Atlas is a personal project, not affiliated with or endorsed by AusTraits or its contributing institutions. Provided as is, for general interest: Not horticultural, ecological or agricultural advice.

* Brief Overview of AusTraits database (dated in this project: 12/09/2026):

"AusTraits is a transformative database, containing measurements on the traits of Australia's plant taxa, standardised from hundreds of disconnected primary sources. So far, data have been assembled from > 300 distinct sources, describing > 500 plant traits and > 34,000 taxa." Falster, D. et al. (2025) “AusTraits: a curated plant trait database for the Australian flora”, Scientific Data. Zenodo. Available at: https://doi.org/10.5281/zenodo.15718081.
