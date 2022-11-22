import os

from aio_proxy.response.helpers import (
    format_bool_field,
    format_collectivite_territoriale,
    format_dirigeants,
    format_ess,
    get_value,
)
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV")


def format_response(results):
    """Format API response to follow a specific schema."""
    formatted_results = []
    for result in results:

        def get_field(field, default=None):
            return get_value(result, field, default)

        result_formatted = {
            "siren": get_field("siren"),
            "nom_complet": get_field("nom_complet"),
            "nombre_etablissements": int(get_field("nombre_etablissements", default=1)),
            "nombre_etablissements_ouverts": int(
                get_field("nombre_etablissements_ouverts", default=0)
            ),
            "siege": {
                "siret": get_field("siret_siege"),
                "date_creation": get_field("date_creation_siege"),
                "tranche_effectif_salarie": get_field("tranche_effectif_salarie_siege"),
                "date_debut_activite": get_field("date_debut_activite_siege"),
                "etat_administratif": get_field("etat_administratif_siege"),
                "activite_principale": get_field("activite_principale_siege"),
                "complement_adresse": get_field("complement_adresse"),
                "numero_voie": get_field("numero_voie"),
                "indice_repetition": get_field("indice_repetition"),
                "type_voie": get_field("type_voie"),
                "libelle_voie": get_field("libelle_voie"),
                "distribution_speciale": get_field("distribution_speciale"),
                "cedex": get_field("cedex"),
                "libelle_cedex": get_field("libelle_cedex"),
                "commune": get_field("commune"),
                "libelle_commune": get_field("libelle_commune"),
                "code_pays_etranger": get_field("code_pays_etranger"),
                "libelle_commune_etranger": get_field("libelle_commune_etranger"),
                "libelle_pays_etranger": get_field("libelle_pays_etranger"),
                "adresse_complete": get_field("adresse_etablissement"),
                "adresse_complete_secondaire": get_field("adresse_etablissement_2"),
                "code_postal": get_field("code_postal"),
                "departement": get_field("departement"),
                "geo_id": get_field("geo_id"),
                "longitude": get_field("longitude"),
                "latitude": get_field("latitude"),
                "activite_principale_registre_metier": get_field(
                    "activite_principale_registre_metier"
                ),
            },
            "date_creation": get_field("date_creation_unite_legale"),
            "tranche_effectif_salarie": get_field(
                "tranche_effectif_salarie_unite_legale"
            ),
            "date_mise_a_jour": get_field("date_mise_a_jour_unite_legale"),
            "categorie_entreprise": get_field("categorie_entreprise"),
            "etat_administratif": get_field("etat_administratif_unite_legale"),
            "nom_raison_sociale": get_field("nom_raison_sociale"),
            "nature_juridique": get_field("nature_juridique_unite_legale"),
            "activite_principale": get_field("activite_principale_unite_legale"),
            "section_activite_principale": get_field("section_activite_principale"),
            "dirigeants": format_dirigeants(
                get_field("dirigeants_pp"), get_field("dirigeants_pm")
            ),
            "complements": {
                "collectivite_territoriale": format_collectivite_territoriale(
                    get_field("colter_code"),
                    get_field("colter_code_insee"),
                    get_field("colter_elus"),
                    get_field("colter_niveau"),
                ),
                "convention_collective_renseignee": format_bool_field(
                    get_field("liste_idcc"),
                ),
                "est_entrepreneur_individuel": get_field(
                    "est_entrepreneur_individuel", default=False
                ),
                "est_entrepreneur_spectacle": format_bool_field(
                    get_field("est_entrepreneur_spectacle")
                ),
                "est_ess": format_ess(
                    get_field("economie_sociale_solidaire_unite_legale")
                ),
                "est_finess": format_bool_field(get_field("liste_finess")),
                "est_rge": format_bool_field(get_field("liste_rge")),
                "est_uai": format_bool_field(get_field("liste_uai")),
                "identifiant_association": get_field(
                    "identifiant_association_unite_legale"
                ),
            },
        }
        # Include score field for dev environment
        if env == "dev":
            result_formatted["score"] = get_field("meta")
        formatted_results.append(result_formatted)
    return formatted_results
