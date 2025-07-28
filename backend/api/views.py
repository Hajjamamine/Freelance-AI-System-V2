import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))



from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from Recommendation_RAG.rag_engine import get_recommendation

class RecommendationView(APIView):
    def post(self, request):
        query = request.data.get("query")
        if not query:
            return Response({"error": "Missing 'query' field."}, status=400)
        try:
            result = get_recommendation(query)
            return Response(result, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

