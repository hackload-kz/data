open System.IO

let transliterate (name: string) : string =
    // Define a map for transliteration from Cyrillic to Latin
    let transliterationMap = 
        [ ('а', "a"); ('б', "b"); ('в', "v"); ('г', "g"); ('д', "d")
          ('е', "e"); ('ё', "yo"); ('ж', "zh"); ('з', "z"); ('и', "i")
          ('й', "y"); ('к', "k"); ('л', "l"); ('м', "m"); ('н', "n")
          ('о', "o"); ('п', "p"); ('р', "r"); ('с', "s"); ('т', "t")
          ('у', "u"); ('ф', "f"); ('х', "kh"); ('ц', "ts"); ('ч', "ch")
          ('ш', "sh"); ('щ', "shch"); ('ъ', "'");  // hard sign
          ('ы', "y");  // yeri
          ('ь', "")    // soft sign
          ('э', "e'");  // e
          ('ю', "yu");  // yu
          ('я', "ya");  // yu
          ('ә', "a"); ('ғ', "g"); ('қ', "q"); ('ң', "n"); ('ө', "o")
          ('ұ', "u"); ('ү', "u"); ('Һ', "h") ] |> Map.ofList

    let transliterated = 
        name.ToLower()
        |> Seq.fold (fun acc c ->
            match Map.tryFind c transliterationMap with
            | Some translit -> acc + translit
            | None -> acc + string c) ""
    transliterated.ToUpperInvariant()

let transliterate_file filename header =
    let names = 
        File.ReadAllLines filename 
        |> Seq.skip 1
        |> Seq.map (fun line -> line.Split(','))
        |> Seq.map (fun parts -> 
            let transliterated = transliterate parts.[1]
            $"{parts[0]},{parts[1]},{transliterated}")
        |> Seq.toList

    File.WriteAllLines(filename, [ header ]  @ names)

transliterate_file "first_names.csv" "Sex,NameKZ,NameEn"
transliterate_file "last_names.csv" "Sex,NameKZ,NameEn"