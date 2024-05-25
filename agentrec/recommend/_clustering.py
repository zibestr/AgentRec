from agents._abstract import _AbstractPopulation
from recommend._abstract import _AbstactRecommendationAlgorithm
import numpy as np
from sklearn.cluster import KMeans
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')


class ClusteringSystem(_AbstactRecommendationAlgorithm):
    def __init__(self, population: _AbstractPopulation):
        super().__init__(population)
        self._clustering = KMeans(n_clusters=int(
            config['ranking']['ClustersCount'])
        )
        self.__predicted_clusters = np.zeros(self._population.size)

    @property
    def preference_matrix(self):
        return np.vstack([agent.ratings for agent in self._population.agents])

    def get_similar_user(self, user_number: int) -> int | None:
        user_ratings = self._population.agents[user_number].ratings
        cluster = self._clustering.predict(
            [user_ratings]
        )[0]
        distance_to_centroid = self._clustering.transform(
            [user_ratings]
        )[0, cluster]

        users_matrix = self.preference_matrix
        users_in_cluster = tuple(
            map(lambda user: user[0],
                filter(lambda user: user[1] == cluster,
                       enumerate(self.__predicted_clusters))
                )
        )
        distances = enumerate(self._clustering.transform(
                users_matrix
        )[:, cluster].flatten())
        normalized_distances = map(
            lambda user: (user[0], abs(user[1] - distance_to_centroid)),
            filter(
                lambda distance: distance[0] in users_in_cluster,
                distances
            )
        )
        sorted_distances = sorted(
            normalized_distances,
            key=lambda value: value[1]
        )

        if len(sorted_distances) == 0:
            return None
        return sorted_distances[0][0]

    def make_recommendation(self, user_number: int) -> int | None:
        recommended_user = self.get_similar_user(user_number)
        if recommended_user is None:
            return None
        recommended_ratings = self._population.agents[recommended_user].ratings
        user_ratings = self._population.agents[user_number].ratings
        recommendations = [i for i, pair in enumerate(zip(recommended_ratings,
                                                          user_ratings))
                           if pair[0] != 0 and pair[1] == 0]
        return recommendations[0] if len(recommendations) != 0 else None

    def train(self):
        self.__predicted_clusters = self._clustering.fit_predict(
            self.preference_matrix
        )
