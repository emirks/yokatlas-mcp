import asyncio  # Required for async yokatlas_py functions
from typing import Literal, Annotated
from pydantic import Field

from fastmcp import FastMCP

# Import the new smart search functions (v0.4.3+)
try:
    from yokatlas_py import search_lisans_programs, search_onlisans_programs
    from yokatlas_py import YOKATLASLisansAtlasi, YOKATLASOnlisansAtlasi
    from yokatlas_py.models import SearchParams, ProgramInfo

    NEW_SMART_API = True
except ImportError:
    # Fallback to older API structure
    try:
        from yokatlas_py import (
            YOKATLASLisansTercihSihirbazi,
            YOKATLASOnlisansTercihSihirbazi,
        )
        from yokatlas_py import YOKATLASLisansAtlasi, YOKATLASOnlisansAtlasi
        from yokatlas_py.models import SearchParams, ProgramInfo

        NEW_SMART_API = False
    except ImportError:
        # Final fallback to very old structure
        from yokatlas_py.lisansatlasi import YOKATLASLisansAtlasi
        from yokatlas_py.lisanstercihsihirbazi import YOKATLASLisansTercihSihirbazi
        from yokatlas_py.onlisansatlasi import YOKATLASOnlisansAtlasi
        from yokatlas_py.onlisanstercihsihirbazi import YOKATLASOnlisansTercihSihirbazi

        NEW_SMART_API = False

# Create a FastMCP server instance
mcp = FastMCP("YOKATLAS API Server")


# Tool for YOKATLAS Onlisans Atlasi
@mcp.tool()
async def get_associate_degree_atlas_details(
    yop_kodu: Annotated[
        str,
        Field(
            description="Program YÖP code (e.g., '120910060') - unique identifier for the associate degree program"
        ),
    ],
    year: Annotated[
        int,
        Field(
            description="Data year for statistics (e.g., 2024, 2023)", ge=2020, le=2030
        ),
    ],
) -> dict:
    """
    Get comprehensive details for a specific associate degree program from YOKATLAS Atlas.

    Parameters:
    - yop_kodu (str): Program YÖP code (e.g., '120910060')
    - year (int): Data year (e.g., 2024, 2023)

    Returns detailed information including:
    - General program information and statistics
    - Quota, placement, and score data
    - Student demographics and distribution
    - Academic staff and facility information
    - Historical placement trends
    """
    try:
        onlisans_atlasi = YOKATLASOnlisansAtlasi({"program_id": yop_kodu, "year": year})
        result = await onlisans_atlasi.fetch_all_details()
        return result
    except Exception as e:
        # Log error or handle it as appropriate for your MCP server
        # For now, re-raising or returning an error structure
        print(f"Error in get_associate_degree_atlas_details: {e}")
        return {"error": str(e), "program_id": yop_kodu, "year": year}


# Tool for YOKATLAS Lisans Atlasi
@mcp.tool()
async def get_bachelor_degree_atlas_details(
    yop_kodu: Annotated[
        str,
        Field(
            description="Program YÖP code (e.g., '102210277') - unique identifier for the bachelor's degree program"
        ),
    ],
    year: Annotated[
        int,
        Field(
            description="Data year for statistics (e.g., 2024, 2023)", ge=2020, le=2030
        ),
    ],
) -> dict:
    """
    Get comprehensive details for a specific bachelor's degree program from YOKATLAS Atlas.

    Parameters:
    - yop_kodu (str): Program YÖP code (e.g., '102210277')
    - year (int): Data year (e.g., 2024, 2023)

    Returns detailed information including:
    - General program information and statistics
    - Quota, placement, and score data
    - Student demographics and distribution
    - Academic staff and facility information
    - Historical placement trends
    """
    try:
        lisans_atlasi = YOKATLASLisansAtlasi({"program_id": yop_kodu, "year": year})
        result = await lisans_atlasi.fetch_all_details()
        return result
    except Exception as e:
        print(f"Error in get_bachelor_degree_atlas_details: {e}")
        return {"error": str(e), "program_id": yop_kodu, "year": year}


# Tool for YOKATLAS Lisans Search with Smart Features
@mcp.tool()
def search_bachelor_degree_programs(
    # User-friendly parameters with fuzzy matching
    university: Annotated[
        str,
        Field(
            description="University name with fuzzy matching support (e.g., 'boğaziçi' → 'BOĞAZİÇİ ÜNİVERSİTESİ')"
        ),
    ] = "",
    program: Annotated[
        str,
        Field(
            description="Program/department name with partial matching (e.g., 'bilgisayar' finds all computer programs)"
        ),
    ] = "",
    city: Annotated[
        str, Field(description="City name where the university is located")
    ] = "",
    score_type: Annotated[
        Literal["SAY", "EA", "SOZ", "DIL"],
        Field(
            description="Score type: SAY (Science), EA (Equal Weight), SOZ (Verbal), DIL (Language)"
        ),
    ] = "SAY",
    university_type: Annotated[
        Literal["", "Devlet", "Vakıf", "KKTC", "Yurt Dışı"],
        Field(
            description="University type: Devlet (State), Vakıf (Foundation), KKTC (TRNC), Yurt Dışı (International)"
        ),
    ] = "",
    fee_type: Annotated[
        Literal[
            "",
            "Ücretsiz",
            "Ücretli",
            "İÖ-Ücretli",
            "Burslu",
            "%50 İndirimli",
            "%25 İndirimli",
            "AÖ-Ücretli",
            "UÖ-Ücretli",
        ],
        Field(
            description="Fee status: Ücretsiz (Free), Ücretli (Paid), İÖ-Ücretli (Evening-Paid), Burslu (Scholarship), İndirimli (Discounted), AÖ-Ücretli (Open Education-Paid), UÖ-Ücretli (Distance Learning-Paid)"
        ),
    ] = "",
    education_type: Annotated[
        Literal["", "Örgün", "İkinci", "Açıköğretim", "Uzaktan"],
        Field(
            description="Education type: Örgün (Regular), İkinci (Evening), Açıköğretim (Open Education), Uzaktan (Distance Learning)"
        ),
    ] = "",
    availability: Annotated[
        Literal["", "Doldu", "Doldu#", "Dolmadı", "Yeni"],
        Field(
            description="Program availability: Doldu (Filled), Doldu# (Filled with conditions), Dolmadı (Not filled), Yeni (New program)"
        ),
    ] = "",
    results_limit: Annotated[
        int, Field(description="Maximum number of results to return", ge=1, le=500)
    ] = 50,
    # Legacy parameter support for backward compatibility
    uni_adi: str = "",
    program_adi: str = "",
    sehir: str = "",
    puan_turu: str = "",
    universite_turu: str = "",
    ucret_burs: str = "",
    ogretim_turu: str = "",
    length: int = 0,
) -> dict:
    """
    Search for bachelor's degree programs with smart fuzzy matching and user-friendly parameters.

    Smart Features:
    - Fuzzy university name matching (e.g., "boğaziçi" → "BOĞAZİÇİ ÜNİVERSİTESİ")
    - Partial program name matching (e.g., "bilgisayar" finds all computer programs)
    - Intelligent parameter normalization
    - Type-safe validation

    Parameters:
    - university: University name (fuzzy matching supported)
    - program: Program/department name (partial matching supported)
    - city: City name
    - score_type: Score type (SAY, EA, SOZ, DIL)
    - university_type: Type of university (Devlet, Vakıf, etc.)
    - fee_type: Fee/scholarship information
    - education_type: Type of education (Örgün, İkinci, etc.)
    - results_limit: Maximum number of results to return
    """
    try:
        if NEW_SMART_API:
            # Use new smart search functions (v0.4.3+)
            search_params = {}

            # Map user-friendly parameters to API parameters
            if university or uni_adi:
                search_params["uni_adi"] = university or uni_adi
            if program or program_adi:
                search_params["program_adi"] = program or program_adi
            if city or sehir:
                search_params["city"] = city or sehir
            if score_type or puan_turu:
                search_params["score_type"] = score_type or puan_turu
            if university_type or universite_turu:
                search_params["university_type"] = university_type or universite_turu
            if fee_type or ucret_burs:
                search_params["fee_type"] = fee_type or ucret_burs
            if education_type or ogretim_turu:
                search_params["education_type"] = education_type or ogretim_turu
            if results_limit or length:
                search_params["length"] = results_limit or length

            # Use smart search with fuzzy matching
            results = search_lisans_programs(search_params, smart_search=True)

            # Validate and format results
            validated_results = []
            for program_data in results:
                try:
                    program = ProgramInfo(**program_data)
                    validated_results.append(program.model_dump())
                except Exception:
                    # Include unvalidated data if validation fails
                    validated_results.append(program_data)

            return {
                "programs": validated_results,
                "total_found": len(validated_results),
                "search_method": "smart_search_v0.4.3",
                "fuzzy_matching": True,
            }

        else:
            # Fallback to legacy API
            params = {
                "uni_adi": university or uni_adi,
                "program_adi": program or program_adi,
                "sehir_adi": city or sehir,
                "puan_turu": (
                    (score_type or puan_turu).lower()
                    if (score_type or puan_turu)
                    else "say"
                ),
                "universite_turu": university_type or universite_turu,
                "ucret_burs": fee_type or ucret_burs,
                "ogretim_turu": education_type or ogretim_turu,
                "page": 1,
            }

            # Remove empty parameters
            params = {k: v for k, v in params.items() if v}

            lisans_tercih = YOKATLASLisansTercihSihirbazi(params)
            result = lisans_tercih.search()

            return {
                "programs": (
                    result[:results_limit] if isinstance(result, list) else result
                ),
                "total_found": len(result) if isinstance(result, list) else 0,
                "search_method": "legacy_api",
                "fuzzy_matching": False,
            }

    except Exception as e:
        print(f"Error in search_bachelor_degree_programs: {e}")
        return {
            "error": str(e),
            "search_method": "smart_search" if NEW_SMART_API else "legacy_api",
            "parameters_used": {
                "university": university or uni_adi,
                "program": program or program_adi,
                "city": city or sehir,
            },
        }


# Tool for YOKATLAS Onlisans Search with Smart Features
@mcp.tool()
def search_associate_degree_programs(
    # User-friendly parameters with fuzzy matching
    university: Annotated[
        str,
        Field(
            description="University name with fuzzy matching support (e.g., 'anadolu' → 'ANADOLU ÜNİVERSİTESİ')"
        ),
    ] = "",
    program: Annotated[
        str,
        Field(
            description="Program name with partial matching (e.g., 'turizm' finds all tourism programs)"
        ),
    ] = "",
    city: Annotated[
        str, Field(description="City name where the university is located")
    ] = "",
    university_type: Annotated[
        Literal["", "Devlet", "Vakıf", "KKTC", "Yurt Dışı"],
        Field(
            description="University type: Devlet (State), Vakıf (Foundation), KKTC (TRNC), Yurt Dışı (International)"
        ),
    ] = "",
    fee_type: Annotated[
        Literal[
            "",
            "Ücretsiz",
            "Ücretli",
            "İÖ-Ücretli",
            "Burslu",
            "%50 İndirimli",
            "%25 İndirimli",
            "AÖ-Ücretli",
            "UÖ-Ücretli",
        ],
        Field(
            description="Fee status: Ücretsiz (Free), Ücretli (Paid), İÖ-Ücretli (Evening-Paid), Burslu (Scholarship), İndirimli (Discounted), AÖ-Ücretli (Open Education-Paid), UÖ-Ücretli (Distance Learning-Paid)"
        ),
    ] = "",
    education_type: Annotated[
        Literal["", "Örgün", "İkinci", "Açıköğretim", "Uzaktan"],
        Field(
            description="Education type: Örgün (Regular), İkinci (Evening), Açıköğretim (Open Education), Uzaktan (Distance Learning)"
        ),
    ] = "",
    availability: Annotated[
        Literal["", "Doldu", "Doldu#", "Dolmadı", "Yeni"],
        Field(
            description="Program availability: Doldu (Filled), Doldu# (Filled with conditions), Dolmadı (Not filled), Yeni (New program)"
        ),
    ] = "",
    results_limit: Annotated[
        int, Field(description="Maximum number of results to return", ge=1, le=500)
    ] = 50,
    # Legacy parameter support for backward compatibility
    yop_kodu: str = "",
    uni_adi: str = "",
    program_adi: str = "",
    sehir_adi: str = "",
    universite_turu: str = "",
    ucret_burs: str = "",
    ogretim_turu: str = "",
    doluluk: str = "",
    ust_puan: float = 550.0,
    alt_puan: float = 150.0,
    page: int = 1,
) -> dict:
    """
    Search for associate degree (önlisans) programs with smart fuzzy matching and user-friendly parameters.

    Smart Features:
    - Fuzzy university name matching (e.g., "anadolu" → "ANADOLU ÜNİVERSİTESİ")
    - Partial program name matching (e.g., "turizm" finds all tourism programs)
    - Intelligent parameter normalization
    - Type-safe validation

    Parameters:
    - university: University name (fuzzy matching supported)
    - program: Program/department name (partial matching supported)
    - city: City name
    - university_type: Type of university (Devlet, Vakıf, etc.)
    - fee_type: Fee/scholarship information
    - education_type: Type of education (Örgün, İkinci, etc.)
    - results_limit: Maximum number of results to return

    Note: Associate degree programs use TYT scores, not SAY/EA/SOZ/DIL like bachelor programs.
    """
    try:
        if NEW_SMART_API:
            # Use new smart search functions (v0.4.3+)
            search_params = {}

            # Map user-friendly parameters to API parameters
            if university or uni_adi:
                search_params["uni_adi"] = university or uni_adi
            if program or program_adi:
                search_params["program_adi"] = program or program_adi
            if city or sehir_adi:
                search_params["city"] = city or sehir_adi
            if university_type or universite_turu:
                search_params["university_type"] = university_type or universite_turu
            if fee_type or ucret_burs:
                search_params["fee_type"] = fee_type or ucret_burs
            if education_type or ogretim_turu:
                search_params["education_type"] = education_type or ogretim_turu
            if results_limit:
                search_params["length"] = results_limit

            # Use smart search with fuzzy matching
            results = search_onlisans_programs(search_params, smart_search=True)

            # Format results consistently
            return {
                "programs": results,
                "total_found": len(results),
                "search_method": "smart_search_v0.4.3",
                "fuzzy_matching": True,
                "program_type": "associate_degree",
            }

        else:
            # Fallback to legacy API
            params = {
                "yop_kodu": yop_kodu,
                "uni_adi": university or uni_adi,
                "program_adi": program or program_adi,
                "sehir_adi": city or sehir_adi,
                "universite_turu": university_type or universite_turu,
                "ucret_burs": fee_type or ucret_burs,
                "ogretim_turu": education_type or ogretim_turu,
                "doluluk": doluluk,
                "ust_puan": ust_puan,
                "alt_puan": alt_puan,
                "page": page,
            }

            # Remove empty parameters
            params = {
                k: v for k, v in params.items() if v or isinstance(v, (int, float))
            }

            onlisans_tercih = YOKATLASOnlisansTercihSihirbazi(params)
            result = onlisans_tercih.search()

            return {
                "programs": (
                    result[:results_limit] if isinstance(result, list) else result
                ),
                "total_found": len(result) if isinstance(result, list) else 0,
                "search_method": "legacy_api",
                "fuzzy_matching": False,
                "program_type": "associate_degree",
            }

    except Exception as e:
        print(f"Error in search_associate_degree_programs: {e}")
        return {
            "error": str(e),
            "search_method": "smart_search" if NEW_SMART_API else "legacy_api",
            "parameters_used": {
                "university": university or uni_adi,
                "program": program or program_adi,
                "city": city or sehir_adi,
            },
            "program_type": "associate_degree",
        }


def main():
    """Main entry point for the YOKATLAS MCP server."""
    import sys
    import os

    # Get port from environment variable (required by Smithery)
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"

    # Check if running in stdio mode for MCP clients
    if "--stdio" in sys.argv:
        print("Starting YOKATLAS API MCP Server in stdio mode for MCP clients...")
        mcp.run(transport="stdio")
    else:
        # Use FastMCP's HTTP server (compatible with Smithery AI)
        print("Starting YOKATLAS API MCP Server with HTTP transport...")
        print(f"Server will be available at http://{host}:{port}")
        print("Smithery AI compatible endpoint: /mcp")

        try:
            # Use FastMCP's run_http method for Smithery compatibility
            mcp.run_http(host=host, port=port)
        except Exception as e:
            print(f"Error starting server: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
